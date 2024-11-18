import functools
import glob
import os
import sys
import h5py
import numpy as np
import psutil
import ray
import open3d as o3d
import skimage.io
import skimage.transform
from scipy.spatial.transform import Rotation as RR
import copy
from enum import Enum

import pcd_mesh_utils as pm_util
import recons_eval_metric as metric
from emopt5views import EMOpt5Views
from seg.seg_const import IMG_SHAPE
from seg.seg_model import ASPP_UNet
from seg.utils import predict_teeth_contour

# 定义常量
RECONS_IMG_WIDTH = 800
SSM_DIR = r"./data/ssm/"  # 假设SSM数据存储在该目录
NUM_PC = 20  # 假设主成分数量为20
PHOTO_DIR = r"./data/photos/"  # 假设照片数据存储在该目录
REF_MESH_DIR = r"./data/ref_mesh/"  # 假设参考网格数据存储在该目录
VIS_DIR = r"./data/vis/"  # 假设可视化结果存储在该目录
REGIS_PARAM_DIR = r"./data/cpdGpParams/"  # 假设配准参数存储在该目录

# 定义照片类型枚举
class PHOTO(Enum):
    UPPER = 'UPPER'
    LOWER = 'LOWER'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    FRONTAL = 'FRONTAL'

PHOTO_TYPES = [PHOTO.UPPER, PHOTO.LOWER, PHOTO.LEFT, PHOTO.RIGHT, PHOTO.FRONTAL]

# 定义其他常量
UPPER_INDICES = [11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27]
LOWER_INDICES = [31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 44, 45, 46, 47]

# 配置
TEMP_DIR = r"./demo/_temp/"
os.makedirs(TEMP_DIR, exist_ok=True)
NUM_CPUS = psutil.cpu_count(logical=False)
print = functools.partial(print, flush=True)
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1200

# 加载预训练的分割模型
def load_trained_model():
    weight_ckpt = r".\seg\weights\weights-teeth-boundary-model.h5"
    model = ASPP_UNet(IMG_SHAPE, filters=[16, 32, 64, 128, 256])
    model.load_weights(weight_ckpt)
    return model

# 加载和预处理图像
def load_and_preprocess_image(image_path):
    image = skimage.io.imread(image_path)
    image = skimage.transform.resize(image, (IMG_SHAPE[0], IMG_SHAPE[1]), anti_aliasing=True)
    image = image.astype(np.float32) / 255.0
    image = np.expand_dims(image, axis=0)  # 添加批次维度
    return image

# 加载SSM参数
def loadMuEigValSigma(ssmDir, numPC):
    muNpys = glob.glob(os.path.join(ssmDir, "meanAlignedPG_*.npy"))
    muNpys = sorted(muNpys, key=lambda x: int(os.path.basename(x).split(".")[0].split("_")[-1]))
    Mu = np.array([np.load(x) for x in muNpys])
    eigValNpys = glob.glob(os.path.join(ssmDir, "eigVal_*.npy"))
    eigValNpys = sorted(eigValNpys, key=lambda x: int(os.path.basename(x).split(".")[0].split("_")[-1]))
    sqrtEigVals = np.sqrt(np.array([np.load(x) for x in eigValNpys]))
    eigVecNpys = glob.glob(os.path.join(ssmDir, "eigVec_*.npy"))
    eigVecNpys = sorted(eigVecNpys, key=lambda x: int(os.path.basename(x).split(".")[0].split("_")[-1]))
    Sigma = np.array([np.load(x) for x in eigVecNpys])

    print(f"Mu shape: {Mu.shape}")
    print(f"sqrtEigVals shape: {sqrtEigVals.shape}")
    print(f"Sigma shape: {Sigma.shape}")

    return Mu, sqrtEigVals[:, np.newaxis, :numPC], Sigma[..., :numPC]

# 运行EM优化
def run_emopt(emopt: EMOpt5Views, verbose: bool = False):
    print("-" * 100)
    print("Start optimization.")
    print("-" * 100)
    print("Start Grid Search.")

    emopt.searchDefaultRelativePoseParams()
    emopt.gridSearchExtrinsicParams()
    emopt.gridSearchRelativePoseParams()

    emopt.expectation_step_5Views(-1, verbose)
    min_e_loss = emopt.get_e_loss()
    optParamDict = emopt.get_current_e_step_result()

    maxiter = 20
    stageIter = [10, 5, 10]

    print("-" * 100)
    print("Start Stage 0.")
    stage = 0

    E_loss = []
    for it in range(stageIter[0]):
        emopt.maximization_step_5Views(stage, step=-1, maxiter=maxiter, verbose=False)
        print("M-step loss: {:.4f}".format(emopt.loss_maximization_step))
        emopt.expectation_step_5Views(stage, verbose)
        e_loss = emopt.get_e_loss()
        if e_loss < min_e_loss:
            optParamDict = emopt.get_current_e_step_result()
            min_e_loss = e_loss
        print("Sum of expectation step loss: {:.4f}".format(e_loss))
        if len(E_loss) >= 2 and e_loss >= np.mean(E_loss[-2:]):
            print(
                "Early stop with last 3 e-step loss {:.4f}, {:.4f}, {:.4f}".format(
                    E_loss[-2], E_loss[-1], e_loss
                )
            )
            E_loss.append(e_loss)
            break
        else:
            E_loss.append(e_loss)

    emopt.load_e_step_result_from_dict(optParamDict)
    emopt.expectation_step_5Views(stage, verbose)
    E_loss.append(min_e_loss)

    skipStage1Flag = False
    print("-" * 100)
    print("Start Stage 1.")

    stage = 1
    for it in range(stageIter[1]):
        emopt.maximization_step_5Views(stage, step=-1, maxiter=maxiter, verbose=False)
        print("M-step loss: {:.4f}".format(emopt.loss_maximization_step))
        emopt.expectation_step_5Views(stage, verbose)
        e_loss = emopt.get_e_loss()
        print("Sum of expectation step loss: {:.4f}".format(e_loss))
        if e_loss >= E_loss[-1]:
            if it == 0:
                skipStage1Flag = True
            print(
                "Early stop with last 3 e-step loss {:.4f}, {:.4f}, {:.4f}".format(
                    E_loss[-2], E_loss[-1], e_loss
                )
            )
            break
        else:
            E_loss.append(e_loss)

    if skipStage1Flag == True:
        print("Skip Stage 1; Reverse to Stage 0 final result.")
        emopt.rowScaleXZ = np.ones((2,))
        emopt.load_e_step_result_from_dict(optParamDict)
    else:
        print("Accept Stage 1.")
        print("emopt.rowScaleXZ: ", emopt.rowScaleXZ)
        print("approx tooth scale: ", np.prod(emopt.rowScaleXZ) ** (1 / 3))
        emopt.anistropicRowScale2ScalesAndTransVecs()

    emopt.expectation_step_5Views(stage, verbose)
    e_loss = emopt.get_e_loss()
    optParamDict = emopt.get_current_e_step_result()

    print("-" * 100)
    print("Start Stage 2 and 3.")
    stage = 2
    E_loss = [
        min_e_loss,
    ]
    for it in range(stageIter[2]):
        emopt.maximization_step_5Views(stage, step=2, maxiter=maxiter, verbose=False)
        emopt.maximization_step_5Views(stage, step=3, maxiter=maxiter, verbose=False)
        emopt.maximization_step_5Views(stage=3, step=-1, maxiter=maxiter, verbose=False)
        emopt.maximization_step_5Views(stage, step=1, maxiter=maxiter, verbose=False)
        print("M-step loss: {:.4f}".format(emopt.loss_maximization_step))
        emopt.expectation_step_5Views(stage=3, verbose=verbose)
        e_loss = emopt.get_e_loss()
        if e_loss < min_e_loss:
            optParamDict = emopt.get_current_e_step_result()
            min_e_loss = e_loss
        print("Sum of expectation step loss: {:.4f}".format(e_loss))
        if len(E_loss) >= 2 and (e_loss >= np.mean(E_loss[-2:])):
            print(
                "Early stop with last 3 e-step loss {:.4f}, {:.4f}, {:.4f}".format(
                    E_loss[-2], E_loss[-1], e_loss
                )
            )
            break
        else:
            E_loss.append(e_loss)

    emopt.load_e_step_result_from_dict(optParamDict)
    emopt.expectation_step_5Views(stage=3, verbose=verbose)

    return emopt

# 读取参考网格顶点
def read_demo_mesh_vertices_by_FDI(mesh_dir, tag, FDIs):
    mesh_vertices_by_FDI = []
    for fdi in FDIs:
        mshf = os.path.join(mesh_dir, str(tag), "byFDI", f"Ref_Mesh_Tag={tag}_FDI={fdi}.obj")
        msh = o3d.io.read_triangle_mesh(mshf)
        mesh_vertices_by_FDI.append(np.asarray(msh.vertices, np.float64))
    return mesh_vertices_by_FDI

def generateProjectedMeshImg(
    visualizer,
    ulTeethMshes,
    phType,
    ex_rxyz,
    ex_txyz,
    fx,
    u0,
    v0,
    rela_R,
    rela_t,
    rh,
    rw,
):
    visualizer.clear_geometries()
    ph = phType.value
    msh = None
    if phType in [PHOTO.UPPER, PHOTO.LOWER]:
        msh = copy.deepcopy(ulTeethMshes[ph])
    else:  # [PHOTO.LEFT, PHOTO.RIGHT, PHOTO.FRONTAL]]
        uMsh = copy.deepcopy(ulTeethMshes[0])
        lMsh = copy.deepcopy(ulTeethMshes[1])
        lMsh.rotate(rela_R.T, center=(0, 0, 0))
        lMsh.translate(rela_t)
        msh = uMsh + lMsh  # merge meshes
    rotMat = RR.from_rotvec(ex_rxyz[ph]).as_matrix()
    msh.rotate(rotMat, center=(0, 0, 0))
    msh.translate(ex_txyz[ph])
    visualizer.add_geometry(msh)
    viewControl = visualizer.get_view_control()
    pinholeParams = o3d.camera.PinholeCameraParameters()
    pinholeParams.intrinsic = o3d.camera.PinholeCameraIntrinsic(
        WINDOW_WIDTH, WINDOW_HEIGHT, fx[ph], fx[ph], u0[ph], v0[ph]
    )
    pinholeParams.extrinsic = np.identity(4)
    viewControl.convert_from_pinhole_camera_parameters(
        pinholeParams, allow_arbitrary=True
    )
    visualizer.update_geometry(msh)
    visualizer.poll_events()
    visualizer.update_renderer()

    _u0 = WINDOW_WIDTH / 2 - 0.5
    _v0 = WINDOW_HEIGHT / 2 - 0.5
    img = np.asarray(visualizer.capture_screen_float_buffer(do_render=True))
    tForm = skimage.transform.EuclideanTransform(
        rotation=None,
        translation=np.array([_u0 - u0[ph], _v0 - v0[ph]]),
        dimensionality=2,
    )
    shiftedImg = skimage.transform.warp(img, tForm)
    croppedImg = shiftedImg[:rh, :rw]
    return croppedImg

def readCameraParamsFromH5(h5File):
    with h5py.File(h5File, "r") as f:
        grp = f["EMOPT"]
        ex_rxyz = grp["EX_RXYZ"][:]
        ex_txyz = grp["EX_TXYZ"][:]
        focLth = grp["FOCLTH"][:]
        dpix = grp["DPIX"][:]
        u0 = grp["U0"][:]
        v0 = grp["V0"][:]
        rela_R = grp["RELA_R"][:]
        rela_t = grp["RELA_T"][:]
        return ex_rxyz, ex_txyz, focLth, dpix, u0, v0, rela_R, rela_t

def meshProjection(visualizer, tag):
    upperTeethObj = os.path.join(DEMO_MESH_DIR, str(tag), f"Pred_Upper_Mesh_Tag={tag}.obj")
    lowerTeethObj = os.path.join(DEMO_MESH_DIR, str(tag), f"Pred_Lower_Mesh_Tag={tag}.obj")
    photos = []
    for phtype in PHOTO_TYPES:
        imgfile = glob.glob(os.path.join(PHOTO_DIR, f"{tag}-{phtype.value}.*"))[0]
        img = skimage.io.imread(imgfile)
        h, w = img.shape[:2]
        scale = RECONS_IMG_WIDTH / w
        rimg = skimage.transform.resize(img, (int(h * scale), RECONS_IMG_WIDTH, 3))
        photos.append(rimg)

    ex_rxyz, ex_txyz, focLth, dpix, u0, v0, rela_R, rela_t = readCameraParamsFromH5(
        h5File=f"{TEMP_DIR}/emopt_result.h5"
    )
    fx = focLth / dpix

    _color = [0.55, 0.7, 0.85]
    _alpha = 0.45

    upperTeethO3dMsh = o3d.io.read_triangle_mesh(upperTeethObj)
    upperTeethO3dMsh.paint_uniform_color(_color)
    upperTeethO3dMsh.compute_vertex_normals()

    lowerTeethO3dMsh = o3d.io.read_triangle_mesh(lowerTeethObj)
    lowerTeethO3dMsh.paint_uniform_color(_color)
    lowerTeethO3dMsh.compute_vertex_normals()

    for phType, img in zip(PHOTO_TYPES, photos):
        mshImg = generateProjectedMeshImg(
            visualizer,
            [upperTeethO3dMsh, lowerTeethO3dMsh],
            phType,
            ex_rxyz,
            ex_txyz,
            fx,
            u0,
            v0,
            rela_R,
            rela_t,
            img.shape[0],
            img.shape[1],
        )
        mesh_img_file = os.path.join(VIS_DIR, f"mesh-tag={tag}-{phType}.png")
        skimage.io.imsave(mesh_img_file, skimage.img_as_ubyte(mshImg))

        bkgrd = np.all(mshImg < 0.01, axis=-1)
        _teethRegion = np.tile(~bkgrd[..., None], (1, 1, 3))
        img = img[..., :3]
        np.putmask(
            img, _teethRegion, np.clip(_alpha * mshImg + (1.0 - _alpha) * img, 0.0, 1.0)
        )
        output = img
        output_img_file = os.path.join(VIS_DIR, f"overlay-tag={tag}-{phType}.png")
        skimage.io.imsave(output_img_file, skimage.img_as_ubyte(output))

# 主流程
def main(tag="0"):
    Mu, SqrtEigVals, Sigma = loadMuEigValSigma(SSM_DIR, numPC=NUM_PC)
    Mu_normals = EMOpt5Views.computePointNormals(Mu)

    transVecStd = 1.1463183505325343
    rotVecStd = 0.13909168140778128
    PoseCovMats = np.load(os.path.join(REGIS_PARAM_DIR, "PoseCovMats.npy"))
    ScaleCovMat = np.load(os.path.join(REGIS_PARAM_DIR, "ScaleCovMat.npy"))

    # 这里需要手动设置牙齿存在的掩码和可见掩码
    tooth_exist_mask = np.array([1] * 28)  # 假设所有牙齿都存在
    visible_masks = [True] * 5  # 假设所有照片都是可见的

    # 加载分割模型
    model = load_trained_model()

    # 预测每张照片中的牙齿边界
    edgeMasks = []
    for phtype in PHOTO_TYPES:
        imgfile = glob.glob(os.path.join(PHOTO_DIR, f"{tag}-{phtype.value}.png"))[0]
        edge_mask = predict_teeth_contour(model, imgfile, resized_width=RECONS_IMG_WIDTH)
        edgeMasks.append(edge_mask)

    mask_u, mask_l = np.split(tooth_exist_mask, 2)
    X_Ref_Upper = read_demo_mesh_vertices_by_FDI(mesh_dir=REF_MESH_DIR, tag=tag, FDIs=np.array(UPPER_INDICES)[mask_u.astype(bool)])
    X_Ref_Lower = read_demo_mesh_vertices_by_FDI(mesh_dir=REF_MESH_DIR, tag=tag, FDIs=np.array(LOWER_INDICES)[mask_l.astype(bool)])

    # 调试打印 PHOTO_TYPES
    print(f"PHOTO_TYPES: {PHOTO_TYPES}")

    # 运行基于变形的3D重建
    emopt = EMOpt5Views(
        edgeMasks,
        PHOTO_TYPES,
        visible_masks,
        tooth_exist_mask.tolist(),
        Mu,
        Mu_normals,
        SqrtEigVals,
        Sigma,
        PoseCovMats,
        ScaleCovMat,
        transVecStd,
        rotVecStd,
    )
    emopt = run_emopt(emopt)
    emopt.saveDemo2H5(f"{TEMP_DIR}/emopt_result.h5")

    # 生成并保存重建网格
    create_mesh_from_emopt_h5File(f"{TEMP_DIR}/emopt_result.h5", meshDir=DEMO_MESH_DIR, save_name=tag)

    # 可视化
    vis = o3d.visualization.Visualizer()
    vis.create_window(
        window_name="Image Screen Shot",
        visible=True,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
    )
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])
    opt.mesh_color_option = o3d.visualization.MeshColorOption.Color  # Normal

    meshProjection(vis, tag)
    vis.destroy_window()

if __name__ == "__main__":
    ray.init(num_cpus=4, num_gpus=0)
    tag = "0"  # 您的图像标记
    main(tag)
