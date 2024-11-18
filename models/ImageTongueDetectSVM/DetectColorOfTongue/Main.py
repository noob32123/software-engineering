# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 08:34:02 2018
SVM Identify the color of Tongues

@author: yfang  yfang0818@gmail.com 
"""


from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import ReferenceExtract
import pickle
from PIL import Image
import os
import numpy as np
import pandas as pd
import TongueDetect
import TrainSVM
import time
import pickle
from PIL import Image
import sklearn.svm.classes
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/tongue', methods=['POST','GET'])
def tongue():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        # 确保目录存在
        print(f"1")
        directory = '../Tongue/new/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        img = Image.open(file.stream)

        # 调整图像大小为 227x227
        #resized_img = img.resize((124, 124))

        # 构建新的文件路径
        resized_path = os.path.join(directory, 'resized_' + 'pic.jpg')

        # 保存调整大小后的图像
        #resized_img.save(resized_path)
        img.save(resized_path)



    data_path1 = '../Tongue/new'
    img_list1 = os.listdir(data_path1)
    print(f"Found {len(img_list1)} images in {data_path1}")
    # img_list1_nosuffix = os.path.splitext(data_path1)[0]

    # #Train the model using data of color references
    # clf=TrainSVM.trainSVM()
    # print(f"Trained SVM model: {clf}")

    # Dump the trained classifier with Pickle
    model_pkl_filename = 'prediction_test_classifier.pkl'

    # Open the file to save as pkl file
    # model_pkl=open(model_pkl_filename,'wb')
    # pickle.dump(clf,model_pkl)

    # close the pickle instances
    # model_pkl.close()
    # 颜色映射字典
    color_map = {
        'jiaohuang': '焦黄',
        'huang': '黄腻舌',
        'hong':'红',
        'danhong': '淡红',
        'bobai': '薄白舌',
        'jiaohei': '焦黑',
        'huihei': '灰黑舌',
       'danbai':'镜面舌',
        'danhuang':'淡黄',
        'bai':'白腻舌',
        'qingzi':'青紫',
        'jiang':'绛红',
        'fanguang':'反光'
    }
    # loading the saved prediction model
    model_pkl = open(model_pkl_filename, 'rb')
    clf = pickle.load(model_pkl)
    # Predict the color of each tongue images
    for img_name in img_list1:
        # Read the color and index
        print('Begin to analysis the color of image', img_name)
        print(time.localtime(time.time()))
        colorImg = Image.open(os.path.join(data_path1, img_name))
        colorPixels = colorImg.convert("RGB")
        colorArray = np.array(colorPixels.getdata()).reshape(colorImg.size + (3,))
        indicesArray = np.moveaxis(np.indices(colorImg.size), 0, 2)
        # reshape the array
        allArray = np.dstack((indicesArray, colorArray)).reshape((-1, 5))

        df = pd.DataFrame(allArray, columns=["col", "row", "red", "green", "blue"])
        # Label each dataframe with the file name
        df["number"] = img_name

        coat, body = TongueDetect.detection(df, clf)
        #print(body)
        coat_hanzi = color_map.get(coat[0][0], coat[0][0])  # 默认返回原始代码
        body_hanzi = color_map.get(body[0][0], body[0][0])  # 默认返回原始代码

        print("舌质和舌苔的颜色分别是", body, coat)

        #return jsonify({'message': f'舌质和舌苔的颜色分别是{body},{coat_hanzi}'})
        return jsonify({'message': f'舌质和舌苔的颜色分别是{body_hanzi},{coat_hanzi}'})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)





# data_path1 = '../Tongues/new'
# img_list1 = os.listdir(data_path1)
# print(f"Found {len(img_list1)} images in {data_path1}")
# #img_list1_nosuffix = os.path.splitext(data_path1)[0]
#
#
# # #Train the model using data of color references
# # clf=TrainSVM.trainSVM()
# # print(f"Trained SVM model: {clf}")
#
#
# #Dump the trained classifier with Pickle
# model_pkl_filename='prediction_test_classifier.pkl'
#
#     #Open the file to save as pkl file
# #model_pkl=open(model_pkl_filename,'wb')
# #pickle.dump(clf,model_pkl)
#
#     #close the pickle instances
# #model_pkl.close()
#
#     #loading the saved prediction model
# model_pkl=open(model_pkl_filename,'rb')
# clf=pickle.load(model_pkl)
# #Predict the color of each tongue images
# for img_name in img_list1:
#     #Read the color and index
#     print('Begin to analysis the color of image',img_name)
#     print (time.localtime(time.time()))
#     colorImg=Image.open(os.path.join(data_path1, img_name))
#     colorPixels=colorImg.convert("RGB")
#     colorArray=np.array(colorPixels.getdata()).reshape(colorImg.size+(3,))
#     indicesArray=np.moveaxis(np.indices(colorImg.size),0,2)
#     #reshape the array
#     allArray=np.dstack((indicesArray,colorArray)).reshape((-1,5))
#
#     df=pd.DataFrame(allArray,columns=["col","row","red","green","blue"])
#     #Label each dataframe with the file name
#     df["number"]=img_name
#
#     coat,body=TongueDetect.detection(df,clf)
#     print("舌质和舌苔的颜色分别是",body,coat)
#
#
#
#
