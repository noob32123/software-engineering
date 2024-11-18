<template>
	<scroll-view class="container">
		<view class="top-section" :style="{ paddingTop: 50 + 'px' }"></view>
		<view class="title-section">
			<image class="sanwei" src="../../static/sanwei.png" @click="changeFake()"></image>
			<view class="title">口腔三维建模</view>
			<view class="total" v-if="!fake">通过按照指定角度拍摄口腔图片，全部上传完毕后点击确定按钮进行口腔三维建模：</view>
		</view>
		<view class="actions" v-if="!confirmed && !fake">
			<view class="action action0">
				<view class="left-photo">
					<image mode="aspectFit" class="left-img" src="../../static/0.png"></image>
					<view class="left-text">请按以上角度拍摄口腔上颚</view>
				</view>
				
				<view class="right-photo">
					<view class="kaishi-container">
						<view class="paizhao-button" @click="takeAPhoto0()" v-if="!photoTaken0&&!photoing0">
							<image class="camera-icon" src="../../static/photo.png"></image>
							<view>上传图片</view>
						</view>
					</view>
					
					<view class="loading1-container"  v-if="!photoTaken0 && photoing0">
						<div class="loading1">
							<div></div>
							<div></div>
							<div></div>
						</div>
						<view>正在上传图片...</view>
					</view>
					
					<view class="photo-result" v-if="photoTaken0 && !photoing0">
						<image
						  :src="photoUrl0"
						  mode="aspectFill"
						  class="photo-result"
						/>
						<view class="restart-button confirm-button" @click="takeAPhoto0()">
							<image class="yes" src="../../static/photo.png"></image>
							<view>重新上传</view>
						</view>
					</view>
				</view>
			</view>
			
			<view class="action action1">
				<view class="left-photo">
					<image mode="aspectFit" class="left-img" src="../../static/1.png"></image>
					<view class="left-text">请按以上角度拍摄口腔下颚</view>
				</view>
				
				<view class="right-photo">
					<view class="kaishi-container">
						<view class="paizhao-button" @click="takeAPhoto1()" v-if="!photoTaken1&&!photoing1">
							<image class="camera-icon" src="../../static/photo.png"></image>
							<view>上传图片</view>
						</view>
					</view>
					
					<view class="loading1-container"  v-if="!photoTaken1 && photoing1">
						<div class="loading1">
							<div></div>
							<div></div>
							<div></div>
						</div>
						<view>正在上传图片...</view>
					</view>
					
					<view class="photo-result" v-if="photoTaken1 && !photoing1">
						<image
						  :src="photoUrl1"
						  mode="aspectFill"
						  class="photo-result"
						/>
						<view class="restart-button confirm-button" @click="takeAPhoto1()">
							<image class="yes" src="../../static/photo.png"></image>
							<view>重新上传</view>
						</view>
					</view>
				</view>
			</view>
			
			<view class="action action2">
				<view class="left-photo">
					<image mode="aspectFit" class="left-img" src="../../static/2.png"></image>
					<view class="left-text">请按以上角度拍摄牙齿左侧</view>
				</view>
				
				<view class="right-photo">
					<view class="kaishi-container">
						<view class="paizhao-button" @click="takeAPhoto2()" v-if="!photoTaken2&&!photoing2">
							<image class="camera-icon" src="../../static/photo.png"></image>
							<view>上传图片</view>
						</view>
					</view>
					
					<view class="loading1-container"  v-if="!photoTaken2 && photoing2">
						<div class="loading1">
							<div></div>
							<div></div>
							<div></div>
						</div>
						<view>正在上传图片...</view>
					</view>
					
					<view class="photo-result" v-if="photoTaken2 && !photoing2">
						<image
						  :src="photoUrl2"
						  mode="aspectFill"
						  class="photo-result"
						/>
						<view class="restart-button confirm-button" @click="takeAPhoto2()">
							<image class="yes" src="../../static/photo.png"></image>
							<view>重新上传</view>
						</view>
					</view>
				</view>
			</view>
			
			<view class="action action3">
				<view class="left-photo">
					<image mode="aspectFit" class="left-img" src="../../static/3.png"></image>
					<view class="left-text">请按以上角度拍摄牙齿右侧</view>
				</view>
				
				<view class="right-photo">
					<view class="kaishi-container">
						<view class="paizhao-button" @click="takeAPhoto3()" v-if="!photoTaken3&&!photoing3">
							<image class="camera-icon" src="../../static/photo.png"></image>
							<view>上传图片</view>
						</view>
					</view>
					
					<view class="loading1-container"  v-if="!photoTaken3 && photoing3">
						<div class="loading1">
							<div></div>
							<div></div>
							<div></div>
						</div>
						<view>正在上传图片...</view>
					</view>
					
					<view class="photo-result" v-if="photoTaken3 && !photoing3">
						<image
						  :src="photoUrl3"
						  mode="aspectFill"
						  class="photo-result"
						/>
						<view class="restart-button confirm-button" @click="takeAPhoto3()">
							<image class="yes" src="../../static/photo.png"></image>
							<view>重新上传</view>
						</view>
					</view>
				</view>
			</view>
			
			<view class="action action4">
				<view class="left-photo">
					<image mode="aspectFit" class="left-img" src="../../static/4.png"></image>
					<view class="left-text">请按以上角度拍摄牙齿正面</view>
				</view>
				
				<view class="right-photo">
					<view class="kaishi-container">
						<view class="paizhao-button" @click="takeAPhoto4()" v-if="!photoTaken4&&!photoing4">
							<image class="camera-icon" src="../../static/photo.png"></image>
							<view>上传图片</view>
						</view>
					</view>
					
					<view class="loading1-container"  v-if="!photoTaken4 && photoing4">
						<div class="loading1">
							<div></div>
							<div></div>
							<div></div>
						</div>
						<view>正在上传图片...</view>
					</view>
					
					<view class="photo-result" v-if="photoTaken4 && !photoing4">
						<image
						  :src="photoUrl4"
						  mode="aspectFill"
						  class="photo-result"
						/>
						<view class="restart-button confirm-button" @click="takeAPhoto4()">
							<image class="yes" src="../../static/photo.png"></image>
							<view>重新上传</view>
						</view>
					</view>
				</view>
			</view>
			
			<view class="paizhao-secion confirm-section">
				<view class="paizhao-button confirm" @click="confirmPhoto()">
					<image class="camera-icon" src="../../static/confirm.png"></image>
					<view>确认图片</view>
				</view>
			</view>
		</view>
		
		<view class="confirm-message" v-if="confirmed && !fake">
			<image class="success" src="../../static/success.png"></image>
			<view class="success-message">已成功将您的口腔资料发送到服务器，分析完成的结果稍后将会发送至您的邮箱</view>
		</view>
		
		<view class="model-result" v-if="fake">
			<view class="model-text">模型分析结果如下:</view>
			<view class="model-text">口腔正面</view>
			<view class="image-item">
				<image class="model-image image-left" mode="aspectFit" src="../../static/mesh_tag_3_PHOTO_FRONTAL.png"></image>
				<image class="model-image image-right" mode="aspectFit"  src="../../static/overlay_tag_3_PHOTO_FRONTAL.png"></image>
			</view>
			<view class="model-text">口腔左侧</view>
			<view class="image-item">
				<image class="model-image image-left" mode="aspectFit" src="../../static/mesh_tag_3_PHOTO_LEFT.png"></image>
				<image class="model-image image-right" mode="aspectFit"  src="../../static/overlay_tag_3_PHOTO_LEFT.png"></image>
			</view>
			<view class="model-text">口腔下部</view>
			<view class="image-item">
				<image class="model-image image-left" mode="aspectFit" src="../../static/mesh_tag_3_PHOTO_LOWER.png"></image>
				<image class="model-image image-right" mode="aspectFit"  src="../../static/overlay_tag_3_PHOTO_LOWER.png"></image>
			</view>
			<view class="model-text">口腔右侧</view>
			<view class="image-item">
				<image class="model-image image-left" mode="aspectFit" src="../../static/mesh_tag_3_PHOTO_RIGHT.png"></image>
				<image class="model-image image-right" mode="aspectFit"  src="../../static/overlay_tag_3_PHOTO_RIGHT.png"></image>
			</view>
			<view class="model-text">口腔上部</view>
			<view class="image-item">
				<image class="model-image image-left" mode="aspectFit" src="../../static/mesh_tag_3_PHOTO_UPPER.png"></image>
				<image class="model-image image-right" mode="aspectFit"  src="../../static/overlay_tag_3_PHOTO_UPPER.png"></image>
			</view>
		</view>
	</scroll-view>
</template>

<script setup>
import { onShow } from "@dcloudio/uni-app"
import { onMounted, ref, reactive, withDirectives} from 'vue'
const baseUrl = "http://192.168.43.42:5173/"
const photoName=ref("")
const confirmed=ref(false)
const fake=ref(false)

const photoTaken0=ref(false)
const photoing0=ref(false)
const photoUrl0=ref("nothing")
const uploadpicname0=ref("")
function changeFake(){
	fake.value=!fake.value
}

function takeAPhoto0(){
	photoTaken0.value=false
	photoing0.value = true
	console.log("开始请求")
	uni.chooseImage({
	    count: 1, // 选择一张图片
	    success: (res) => {
	        const filePath = res.tempFilePaths[0];
			console.log(filePath);
	        // 选择成功后调用上传接口
	        uni.uploadFile({
	            url: baseUrl+"getpictures_30",
	            filePath: filePath,
	            name: 'file',
	            success: (uploadFileRes) => {
	                console.log('上传成功:', uploadFileRes);
					uploadpicname0.value=uploadFileRes.data;
					photoing0.value = false
					photoUrl0.value=baseUrl+`shot_30/`+uploadpicname0.value;
					photoTaken0.value = true; 
	            },
	            fail: (err) => {
	                console.log('上传失败:', err);
	            }
	        });
	    }
	});
}

const photoTaken1=ref(false)
const photoing1=ref(false)
const photoUrl1=ref("nothing")
const uploadpicname1=ref("")
function takeAPhoto1(){
	photoTaken1.value=false
	photoing1.value = true
	uni.chooseImage({
	    count: 1, // 选择一张图片
	    success: (res) => {
	        const filePath = res.tempFilePaths[0];
			console.log(filePath);
	        // 选择成功后调用上传接口
	        uni.uploadFile({
	            url: baseUrl+"getpictures_31",
	            filePath: filePath,
	            name: 'file',
	            success: (uploadFileRes) => {
	                console.log('上传成功:', uploadFileRes);
					uploadpicname1.value=uploadFileRes.data;
					photoing1.value = false
					photoUrl1.value=baseUrl+`shot_31/`+uploadpicname1.value;
					photoTaken1.value = true; 
	            },
	            fail: (err) => {
	                console.log('上传失败:', err);
	            }
	        });
	    }
	});
}

const photoTaken2=ref(false)
const photoing2=ref(false)
const photoUrl2=ref("nothing")
const uploadpicname2=ref("")
function takeAPhoto2(){
	photoTaken2.value=false
	photoing2.value = true
	console.log("开始请求")
	uni.chooseImage({
	    count: 1, // 选择一张图片
	    success: (res) => {
	        const filePath = res.tempFilePaths[0];
			console.log(filePath);
	        // 选择成功后调用上传接口
	        uni.uploadFile({
	            url: baseUrl+"getpictures_32",
	            filePath: filePath,
	            name: 'file',
	            success: (uploadFileRes) => {
	                console.log('上传成功:', uploadFileRes);
					uploadpicname2.value=uploadFileRes.data;
					photoing2.value = false
					photoUrl2.value=baseUrl+`shot_32/`+uploadpicname2.value;
					photoTaken2.value = true; 
	            },
	            fail: (err) => {
	                console.log('上传失败:', err);
	            }
	        });
	    }
	});
}

const photoTaken3=ref(false)
const photoing3=ref(false)
const photoUrl3=ref("nothing")
const uploadpicname3=ref("")
function takeAPhoto3(){
	photoTaken3.value=false
	photoing3.value = true
	console.log("开始请求")
	uni.chooseImage({
	    count: 1, // 选择一张图片
	    success: (res) => {
	        const filePath = res.tempFilePaths[0];
			console.log(filePath);
	        // 选择成功后调用上传接口
	        uni.uploadFile({
	            url: baseUrl+"getpictures_33",
	            filePath: filePath,
	            name: 'file',
	            success: (uploadFileRes) => {
	                console.log('上传成功:', uploadFileRes);
					uploadpicname3.value=uploadFileRes.data;
					photoing3.value = false
					photoUrl3.value=baseUrl+`shot_33/`+uploadpicname3.value;
					photoTaken3.value = true; 
	            },
	            fail: (err) => {
	                console.log('上传失败:', err);
	            }
	        });
	    }
	});
}

const photoTaken4=ref(false)
const photoing4=ref(false)
const photoUrl4=ref("nothing")
const uploadpicname4=ref("")
function takeAPhoto4(){
	photoTaken4.value=false
	photoing4.value = true
	console.log("开始请求")
	uni.chooseImage({
	    count: 1, // 选择一张图片
	    success: (res) => {
	        const filePath = res.tempFilePaths[0];
			console.log(filePath);
	        // 选择成功后调用上传接口
	        uni.uploadFile({
	            url: baseUrl+"getpictures_34",
	            filePath: filePath,
	            name: 'file',
	            success: (uploadFileRes) => {
	                console.log('上传成功:', uploadFileRes);
					uploadpicname4.value=uploadFileRes.data;
					photoing4.value = false
					photoUrl4.value=baseUrl+`shot_34/`+uploadpicname4.value;
					photoTaken4.value = true; 
	            },
	            fail: (err) => {
	                console.log('上传失败:', err);
	            }
	        });
	    }
	});
}

function confirmPhoto(){
	console.log("开始请求")
	uni.request({
		url: baseUrl+'confirm_all',
		method: 'GET',
		header: {
			'Content-Type': 'application/json',
		},
		success: (res) => {
			confirmed.value=true
			console.log('等待邮件发送')
		},
		fail: (err) => {
			console.error('请求失败', err);
		}
	});
}

</script>

<style>
/* 上方说明 */
.title-section{
	display: flex;
	flex-direction: column;
	align-items: center;
	width: 100%;
}
.title{
	margin-top: 18rpx;
	font-weight: bold;
	letter-spacing: 5rpx;
}
.total{
	margin-top: 18rpx;
	font-weight: bold;
	width: 80%;
}
.sanwei{
	width: 200rpx;
	height: 200rpx;
}	
/* 口腔bar */	
.actions{
	display: flex;
	flex-direction: column;
}
.action{
	display: flex;
	justify-content: space-around;
	height: 350rpx;
	margin-top: 30rpx;
}
.left-photo{
	width: 50%;
	font-size: 28rpx;
}

.left-img{
	width: 320rpx;
	height: 240rpx;
	border-radius: 10rpx;
}
.right-photo{
	display: flex;
	justify-content: center;
	width: 320rpx;
}
.photo-result{
	width: 320rpx;
	height: 240rpx;
	border-radius: 10rpx;
}
/******************************/
.confirm-button{
	display: flex;
	align-items: center;
	justify-content: space-around;
	font-size: 32rpx;
	color: white;
	background-image: linear-gradient(to top, #48c6ef 0%, #6f86d6 100%);
	font-weight: bold;
	padding: 18rpx;
	border-radius: 12rpx;
	margin-top: 10rpx;
	box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
}
.restart-button{
	background-image: linear-gradient(60deg, #96deda 0%, #50c9c3 100%);
}
.yes{
	width: 40rpx;
	height: 40rpx;
}
.camera-icon{
	width: 42rpx;
	height: 42rpx;
	border-radius: 50%;
	margin-right: 10rpx;
}
.kaishi-container{
	height: 100%;
	display: flex;
	align-items: center;
}
.paizhao-button{
	width: 240rpx;
	height: 60rpx;
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 10rpx;
	border-radius: 8rpx;
	background-image: linear-gradient(to right, #43e97b 0%, #38f9d7 100%);
	font-weight: bold;
	color: white;
	box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
	margin-bottom: 10rpx;
	
}

/* 拍照加载 */
.loading1-container{
	display: flex;
	align-items: center;
	flex-direction: column;
	justify-content: center;
	margin-top: 20%;
	margin-bottom: 20%;
	font-weight: bold;
	letter-spacing: 1rpx;
}
.loading1{
	margin-bottom: 20%;
}

.loading1,
.loading1 > div {
  position: relative;
  box-sizing: border-box;
}

.loading1 {
  display: block;
  font-size: 0;
  color: #000;
}

.loading1.la-dark {
  color: #333;
}

.loading1 > div {
  display: inline-block;
  float: none;
  background-color: currentColor;
  border: 0 solid currentColor;
}

.loading1 {
  width: 54px;
  height: 18px;
}

.loading1 > div {
  width: 10px;
  height: 10px;
  margin: 4px;
  border-radius: 100%;
  animation: ball-beat 0.7s -0.15s infinite linear;
}

.loading1 > div:nth-child(2n-1) {
  animation-delay: -0.5s;
}

@keyframes ball-beat {
  50% {
    opacity: 0.2;
    transform: scale(0.75);
  }

  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* 确认按钮 */
.confirm-section{
	display: flex;
	justify-content: center;

}
.confirm{
	background-image: linear-gradient(to right, #e9da68 0%, #f98c1f 100%);
}

/* 分析成功 */
.confirm-message{
	display: flex;
	flex-direction: column;
	width: 100%;
	justify-content: center;
	align-items: center;
	margin-top: 30rpx;
}
.success{
	width: 250rpx;
	height: 250rpx;
}
.success-message{
	margin-top: 18rpx;
	font-weight: bold;
	width: 80%;
}

/* 分析结果 */
.model-text{
	display: flex;
	justify-content: center;
	margin: 18rpx;
	font-weight: bold;
}
.image-item{
	display: flex;
	align-items: center;
	justify-content: space-around;
}
.model-image{
	margin: 2rpx;
	height: 250rpx;
}
</style>
			
