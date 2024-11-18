import functools
import glob
import os
import sys
import copy  # 需要导入的模块
import h5py
import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d
import psutil
import ray
import skimage.io  # 需要导入的模块
import skimage.transform  # 需要导入的模块
from scipy.spatial.transform import Rotation as RR  # 需要导入的模块
import copy

import pcd_mesh_utils as pm_util
import recons_eval_metric as metric
from const import *
from emopt5views import EMOpt5Views
from seg.seg_const import IMG_SHAPE
from seg.seg_model import ASPP_UNet
from seg.utils import predict_teeth_contour

from PIL import Image
import os
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/pic30', methods=['POST', 'GET'])
def pic30():
    if 'file' not in request.files:
        # 如果没有文件部分，返回错误信息
        return jsonify({'message': 'No file part'}), 400

    # 从请求中获取文件
    file = request.files['file']
    # 如果没有选择文件，返回错误信息
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # 保存文件到本地路径，并继续处理
    save_path = f'./input_image/3-0.png'
    file.save(save_path)

    return jsonify({'message': 'success'}), 200

@app.route('/pic31', methods=['POST', 'GET'])
def pic31():
    if 'file' not in request.files:
        # 如果没有文件部分，返回错误信息
        return jsonify({'message': 'No file part'}), 400

    # 从请求中获取文件
    file = request.files['file']
    # 如果没有选择文件，返回错误信息
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # 保存文件到本地路径，并继续处理
    save_path = f'./input_image/3-1.png'
    file.save(save_path)

    return jsonify({'message': 'success'}), 200

@app.route('/pic32', methods=['POST', 'GET'])
def pic32():
    if 'file' not in request.files:
        # 如果没有文件部分，返回错误信息
        return jsonify({'message': 'No file part'}), 400

    # 从请求中获取文件
    file = request.files['file']
    # 如果没有选择文件，返回错误信息
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # 保存文件到本地路径，并继续处理
    save_path = f'./input_image/3-2.png'
    file.save(save_path)
    return jsonify({'message': 'success'}), 200

@app.route('/pic33', methods=['POST', 'GET'])
def pic33():
    if 'file' not in request.files:
        # 如果没有文件部分，返回错误信息
        return jsonify({'message': 'No file part'}), 400

    # 从请求中获取文件
    file = request.files['file']
    # 如果没有选择文件，返回错误信息
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # 保存文件到本地路径，并继续处理
    save_path = f'./input_image/3-3.png'
    file.save(save_path)

    return jsonify({'message': 'success'}), 200

@app.route('/pic34', methods=['POST', 'GET'])
def pic34():
    if 'file' not in request.files:
        # 如果没有文件部分，返回错误信息
        return jsonify({'message': 'No file part'}), 400

    # 从请求中获取文件
    file = request.files['file']
    # 如果没有选择文件，返回错误信息
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # 保存文件到本地路径，并继续处理
    save_path = f'./input_image/3-4.png'
    file.save(save_path)

    return jsonify({'message': 'success'}), 200

@app.route('/confirm', methods=['POST', 'GET'])
def confirm():
    TEMP_DIR = r"./demo/_temp/"
    os.makedirs(TEMP_DIR, exist_ok=True)

    PHOTO_DIR = r"./input_image"

    NUM_CPUS = psutil.cpu_count(logical=False)
    # print = functools.partial(print, flush=True)

    def getToothIndex(f):
        return int(os.path.basename(f).split(".")[0].split("_")[-1])

    def loadMuEigValSigma(ssmDir, numPC):
        """Mu.shape=(28,1500,3), sqrtEigVals.shape=(28,1,100), Sigma.shape=(28,4500,100)"""
        muNpys = glob.glob(os.path.join(ssmDir, "meanAlignedPG_*.npy"))
        muNpys = sorted(muNpys, key=lambda x: getToothIndex(x))
        Mu = np.array([np.load(x) for x in muNpys])
        eigValNpys = glob.glob(os.path.join(ssmDir, "eigVal_*.npy"))
        eigValNpys = sorted(eigValNpys, key=lambda x: getToothIndex(x))
        sqrtEigVals = np.sqrt(np.array([np.load(x) for x in eigValNpys]))
        eigVecNpys = glob.glob(os.path.join(ssmDir, "eigVec_*.npy"))
        eigVecNpys = sorted(eigVecNpys, key=lambda x: getToothIndex(x))
        Sigma = np.array([np.load(x) for x in eigVecNpys])
        return Mu, sqrtEigVals[:, np.newaxis, :numPC], Sigma[..., :numPC]

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

    def evaluation(h5File, X_Ref_Upper, X_Ref_Lower):
        """
        h5file: emopt result saved in h5 format
        X_Ref_Upper, X_Ref_Lower: List of numpy arrays
        """
        with h5py.File(h5File, "r") as f:
            grp = f["EMOPT"]
            X_Pred_Upper = grp["UPPER_PRED"][:]
            X_Pred_Lower = grp["LOWER_PRED"][:]

        _X_Ref = X_Ref_Upper + X_Ref_Lower
        print(
            "Compare prediction shape aligned by similarity registration with ground truth."
        )
        with_scale = True
        TX_Upper = pm_util.getAlignedSrcPointCloud(
            X_Pred_Upper.reshape(-1, 3), np.concatenate(X_Ref_Upper), with_scale=with_scale
        )
        TX_Lower = pm_util.getAlignedSrcPointCloud(
            X_Pred_Lower.reshape(-1, 3), np.concatenate(X_Ref_Lower), with_scale=with_scale
        )

        TX_Pred_Upper = TX_Upper.reshape(-1, NUM_POINT, 3)
        TX_Pred_Lower = TX_Lower.reshape(-1, NUM_POINT, 3)
        _TX_Pred = np.concatenate([TX_Pred_Upper, TX_Pred_Lower])

        RMSD_T_pred = metric.computeRMSD(_X_Ref, _TX_Pred)
        ASSD_T_pred = metric.computeASSD(_X_Ref, _TX_Pred)
        HD_T_pred = metric.computeHD(_X_Ref, _TX_Pred)
        CD_T_pred = metric.computeChamferDistance(_X_Ref, _TX_Pred)
        print("[RMSD] Root Mean Squared surface Distance (mm): {:.4f}".format(RMSD_T_pred))
        print("[ASSD] average symmetric surface distance (mm): {:.4f}".format(ASSD_T_pred))
        print("[HD] Hausdorff distance (mm): {:.4f}".format(HD_T_pred))
        print("[CD] Chamfer distance (mm^2): {:.4f}".format(CD_T_pred))

        Dice_VOE_lst = [
            metric.computeDiceAndVOE(_x_ref, _x_pred, pitch=0.2)
            for _x_ref, _x_pred in zip(_X_Ref, _TX_Pred)
        ]
        avg_Dice, avg_VOE = np.array(Dice_VOE_lst).mean(axis=0)
        print("[DC] Volume Dice Coefficient: {:.4f}".format(avg_Dice))
        print("[VOE] Volumetric Overlap Error: {:.2f} %".format(100.0 * avg_VOE))

    def create_mesh_from_emopt_h5File(h5File, meshDir, save_name):
        with h5py.File(h5File, "r") as f:
            grp = f["EMOPT"]
            X_Pred_Upper = grp["UPPER_PRED"][:]
            X_Pred_Lower = grp["LOWER_PRED"][:]

        X_Pred_Upper_Meshes = [
            pm_util.surfaceVertices2WatertightO3dMesh(pg) for pg in X_Pred_Upper
        ]
        X_Pred_Lower_Meshes = [
            pm_util.surfaceVertices2WatertightO3dMesh(pg) for pg in X_Pred_Lower
        ]
        Pred_Upper_Mesh = pm_util.mergeO3dTriangleMeshes(X_Pred_Upper_Meshes)
        Pred_Lower_Mesh = pm_util.mergeO3dTriangleMeshes(X_Pred_Lower_Meshes)

        demoMeshDir = os.path.join(meshDir, "{}/".format(save_name))
        os.makedirs(demoMeshDir, exist_ok=True)

        pm_util.exportTriMeshObj(
            np.asarray(Pred_Upper_Mesh.vertices),
            np.asarray(Pred_Upper_Mesh.triangles),
            os.path.join(demoMeshDir, "Pred_Upper_Mesh_Tag={}.obj".format(save_name)),
        )
        pm_util.exportTriMeshObj(
            np.asarray(Pred_Lower_Mesh.vertices),
            np.asarray(Pred_Lower_Mesh.triangles),
            os.path.join(demoMeshDir, "Pred_Lower_Mesh_Tag={}.obj".format(save_name)),
        )

    def read_demo_mesh_vertices_by_FDI(mesh_dir, tag, FDIs):
        mesh_vertices_by_FDI = []
        for fdi in FDIs:
            mshf = os.path.join(
                mesh_dir, str(tag), "byFDI", f"Ref_Mesh_Tag={tag}_FDI={fdi}.obj"
            )
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
        else:
            uMsh = copy.deepcopy(ulTeethMshes[0])
            lMsh = copy.deepcopy(ulTeethMshes[1])
            lMsh.rotate(rela_R.T, center=(0, 0, 0))
            lMsh.translate(rela_t)
            msh = uMsh + lMsh
        rotMat = RR.from_rotvec(ex_rxyz[ph]).as_matrix()
        msh.rotate(rotMat, center=(0, 0, 0))
        msh.translate(ex_txyz[ph])
        visualizer.add_geometry(msh)
        viewControl = visualizer.get_view_control()
        pinholeParams = o3d.camera.PinholeCameraParameters()
        pinholeParams.intrinsic = o3d.camera.PinholeCameraIntrinsic(
            1600, 1200, fx[ph], fx[ph], u0[ph], v0[ph]
        )
        pinholeParams.extrinsic = np.identity(4)
        viewControl.convert_from_pinhole_camera_parameters(
            pinholeParams, allow_arbitrary=True
        )
        visualizer.update_geometry(msh)
        visualizer.poll_events()
        visualizer.update_renderer()

        _u0 = 1600 / 2 - 0.5
        _v0 = 1200 / 2 - 0.5
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
        demoH5File = os.path.join(DEMO_H5_DIR, f"demo-tag={tag}.h5")
        upperTeethObj = os.path.join(
            DEMO_MESH_DIR, str(tag), r"Pred_Upper_Mesh_Tag={}.obj".format(tag)
        )
        lowerTeethObj = os.path.join(
            DEMO_MESH_DIR, str(tag), r"Pred_Lower_Mesh_Tag={}.obj".format(tag)
        )
        photos = []
        for phtype in PHOTO_TYPES:
            imgfile = glob.glob(os.path.join(PHOTO_DIR, f"{tag}-{phtype.value}.*"))[0]
            img = skimage.io.imread(imgfile)
            h, w = img.shape[:2]
            scale = RECONS_IMG_WIDTH / w
            rimg = skimage.transform.resize(img, (int(h * scale), RECONS_IMG_WIDTH, 3))
            photos.append(rimg)

        ex_rxyz, ex_txyz, focLth, dpix, u0, v0, rela_R, rela_t = readCameraParamsFromH5(
            h5File=demoH5File
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

    def main(tag="0"):
        Mu, SqrtEigVals, Sigma = loadMuEigValSigma(SSM_DIR, numPC=NUM_PC)
        Mu_normals = EMOpt5Views.computePointNormals(Mu)

        transVecStd = 1.1463183505325343
        rotVecStd = 0.13909168140778128
        PoseCovMats = np.load(
            os.path.join(REGIS_PARAM_DIR, "PoseCovMats.npy")
        )
        ScaleCovMat = np.load(
            os.path.join(REGIS_PARAM_DIR, "ScaleCovMat.npy")
        )

        tooth_exist_mask = TOOTH_EXIST_MASK[tag]
        LogFile = os.path.join(TEMP_DIR, "Tag={}.log".format(tag))
        if os.path.exists(LogFile):
            os.remove(LogFile)
        log = open(LogFile, "a", encoding="utf-8")
        sys.stdout = log

        weight_ckpt = r".\seg\weights\weights-teeth-boundary-model.h5"
        model = ASPP_UNet(IMG_SHAPE, filters=[16, 32, 64, 128, 256])
        model.load_weights(weight_ckpt)

        edgeMasks = []
        for i, phtype in enumerate(PHOTO_TYPES):
            imgfile = os.path.join(PHOTO_DIR, f"{tag}-{i}.png")
            if not os.path.exists(imgfile):
                raise FileNotFoundError(f"Image not found: {imgfile}")

            edge_mask = predict_teeth_contour(
                model, imgfile, resized_width=RECONS_IMG_WIDTH
            )
            edgeMasks.append(edge_mask)

        mask_u, mask_l = np.split(tooth_exist_mask, 2)
        X_Ref_Upper = read_demo_mesh_vertices_by_FDI(
            mesh_dir=REF_MESH_DIR, tag=tag, FDIs=np.array(UPPER_INDICES)[mask_u]
        )
        X_Ref_Lower = read_demo_mesh_vertices_by_FDI(
            mesh_dir=REF_MESH_DIR, tag=tag, FDIs=np.array(LOWER_INDICES)[mask_l]
        )

        emopt = EMOpt5Views(
            edgeMasks,
            PHOTO_TYPES,
            VISIBLE_MASKS,
            tooth_exist_mask,
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
        demoh5File = os.path.join(DEMO_H5_DIR, f"demo-tag={tag}.h5")
        emopt.saveDemo2H5(demoh5File)

        create_mesh_from_emopt_h5File(demoh5File, meshDir=DEMO_MESH_DIR, save_name=tag)

        vis = o3d.visualization.Visualizer()
        vis.create_window(
            window_name="Image Screen Shot",
            visible=True,
            width=1600,
            height=1200,
        )
        opt = vis.get_render_option()
        opt.background_color = np.asarray([0, 0, 0])
        opt.mesh_color_option = o3d.visualization.MeshColorOption.Color

        meshProjection(vis, tag)
        vis.destroy_window()

        log.close()

    ray.init(num_cpus=4, num_gpus=0)
    tag = "3"
    main(tag)
    #email
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage

    # SMTP服务器配置
    smtp_server = 'smtp.163.com'  # 替换为你的SMTP服务器
    smtp_port = 25  # 或者465，取决于你的邮箱服务
    username = 'hy24embeddedsystem@163.com'  # 你的邮箱
    password = 'NYdXVa95asbm9K6f'  # 你的邮箱密码

    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = 'yangbochengpersonal@gmail.com'  # 收件人邮箱
    msg['Subject'] = '3-d result'

    # 添加邮件正文
    body = 'this is your result of 3-d modeling'
    msg.attach(MIMEText(body, 'plain'))

    # 图片列表
    image_paths = ['demo/visualization/mesh-tag=3-PHOTO.FRONTAL.png', 'demo/visualization/mesh-tag=3-PHOTO.LEFT.png',
                   'demo/visualization/mesh-tag=3-PHOTO.LOWER.png', 'demo/visualization/mesh-tag=3-PHOTO.RIGHT.png',
                   'demo/visualization/mesh-tag=3-PHOTO.UPPER.png',
                   'demo/visualization/overlay-tag=3-PHOTO.FRONTAL.png',
                   'demo/visualization/overlay-tag=3-PHOTO.LEFT.png',
                   'demo/visualization/overlay-tag=3-PHOTO.LOWER.png',
                   'demo/visualization/overlay-tag=3-PHOTO.RIGHT.png',
                   'demo/visualization/overlay-tag=3-PHOTO.UPPER.png']

    # 附加多个图片
    for image_path in image_paths:
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', f'<{image_path}>')  # 使用文件名作为Content-ID
            img.add_header('Content-Disposition', f'attachment; filename="{image_path.split("/")[-1]}"')
            msg.attach(img)

    # 发送邮件

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # 启用TLS
        server.login(username, password)  # 登录邮箱
        server.send_message(msg)  # 发送邮件





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
