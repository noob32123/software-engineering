<template>
	<scroll-view class="container" scroll-y="true">
		<!-- 拍摄部分 -->
		<view class="photo-section" v-if="!photoTaken">
			<!-- 拍照 -->
			<view class="top-section" :style="{ paddingTop: 50 + 'px' }"></view>
			<view class="take-photo">
				<view class="photo-icon" v-if="!photoSelected && !photoing">
					<image class="kouqiang-icon" src="../../static/shetou.png"></image>
					<view class="paizhao-secion">
						<view class="paizhao-button" @click="takeAPhoto()">
							<image class="camera-icon" src="../../static/photo.png"></image>
							<view>上传图片</view>
						</view>
						<view class="phone-text">请将摄像头按照对准舌苔，确保拍摄角度与上图一致。</view>
					</view>
				</view>
				
				<view class="loading1-container"  v-if="photoing">
					<div class="loading1">
						<div></div>
						<div></div>
						<div></div>
					</div>
					<view>正在上传图片...</view>
				</view>
				
				<view class="photo-result" v-if="photoSelected&&!analyseing&&!photoing">
					<image
					  :src="photoUrl"
					  mode="scaleToFill"
					  class="yachi"
					/>
					<view class="confirm-button-container">
						<view class="restart-button confirm-button" @click="takeAPhoto()">
							<image class="yes" src="../../static/photo.png"></image>
							<view>重新上传</view>
						</view>
						<view class="confirm-button" @click="confirmPhoto()">
							<image class="yes" src="../../static/yes.png"></image>
							<view>确认图片</view>
						</view>
					</view>
				</view>
				
				<view class="loading-container" v-if="photoSelected&&analyseing">
					<div class="loading"></div>
					<view>正在分析消化健康状况...</view>
				</view>
				
			</view>
			
		</view>
		
		<!-- 拍摄结果分析部分 -->
		<view class="analyse-section" v-if="photoTaken">
			<view class="top-section" :style="{ paddingTop: 30 + 'px' }"></view>
			<view class="photo-text">舌苔结果分析</view>
			
			<view class="photo">
				<view class="picture-container">
					<image class="picture" :src="photoUrl" mode="widthFix"></image>
				</view>
			</view>
			
			<view class="zhuangkuang-container">
				<view class="health">
					<view class="zhuangkuang">
						<image
						  src="../../static/oral.png"
						  mode="scaleToFill"
						  class="yachi-picture"
						/>
						舌苔健康状况
					</view>
					<view class="content" v-for="item in resData.condition">
						<view class="fu-title">{{item.title}}</view>
						<view class="yinshi">
							<view class="fu-content" v-for="sen in item.content">{{sen}}</view>
						</view>
					</view>
				</view>
			</view>
			
<!-- 			<view class="zhuangkuang-container">
				<view class="health">
					<view class="zhuangkuang">
						<image
						  src="../../static/digest.png"
						  mode="scaleToFill"
						  class="yachi-picture"
						/>
						ph检测分析
					</view>
					<view class="content">
						<view class="yinshi">
							<view class="fu-content">口腔pH值为6.86,正常口腔PH值范围为6.6-7.0，因此您的口腔PH值在正常范围内。</view>
						</view>
					</view>
				</view>
			</view> -->
	
			<view class="fangan-container">
				<view class="fangan-content">
					<view class="fangan-title">
					  <image
						src="../../static/advice.png"
						mode="scaleToFill"
						class="advice-picture"
					  />
					  护理建议
					</view>
					<view class="fangan-list" v-for="item in resData.analyse">
						<view class="fangan-item" v-for="sentence ,index in item.content">
							<view class="dot dot1" :style="{backgroundColor:textColor[index%3]}"></view>
							<view class="text-section-1" :style="{color:textColor[index%3],backgroundColor:bacColor[index%3]}">
								{{sentence}}
							</view>
						</view>
					</view>
				</view>
			</view>
			
		</view>
	</scroll-view>
</template>

<script setup>
import { onShow } from "@dcloudio/uni-app"
import { onMounted, ref ,reactive} from 'vue'

const bacColor = ["#c2e9fb","#f5efef","#d8fee1"]
const textColor = ["#4481eb","#ed6ea0","#6fe186"]

const photoTaken=ref(false)
const photoSelected=ref(false)
const phSelected=ref(false)
const photoUrl=ref("nothing")
const photoName=ref("")
const baseUrl = "http://192.168.43.42:5173/"
const resData=reactive({
	condition:[],
	analyse:[]
})
const analyseing=ref(false)
const photoing = ref(false)
const ph=ref("")
const uploadpicname=ref("")

function takeAPhoto(){
	photoing.value=true;
	uni.chooseImage({
	    count: 1, // 选择一张图片
	    success: (res) => {
	        const filePath = res.tempFilePaths[0];
			console.log(filePath);
	        // 选择成功后调用上传接口
	        uni.uploadFile({
	            url: baseUrl+"getpictures_tongue",
	            filePath: filePath,
	            name: 'file',
	            success: (uploadFileRes) => {
	                console.log('上传成功:', uploadFileRes);
					uploadpicname.value=uploadFileRes.data;
					photoing.value=false;
					photoSelected.value=true;
					photoUrl.value=baseUrl+`shot_tongue/`+uploadpicname.value;
	            },
	            fail: (err) => {
	                console.log('上传失败:', err);
	            }
	        });
	    }
	});
}

function confirmPhoto(){
	console.log("确认图片")
	console.log(photoName.value)
	analyseing.value=true
	uni.request({
		url: baseUrl+`confirm_shot_tongue/`+uploadpicname.value, // 替换为您的实际API地址
		method: 'GET',
		header: {
			'Content-Type': 'application/json', // 设置请求头
		},
		success: (res) => {
					analyseing.value=false
					console.log(res)
					resData.condition = res.data.message.condition;
					resData.analyse=res.data.message.analyse;
					photoTaken.value=true;
				},
		fail: (err) => {
			console.error('请求失败', err);
		}
	});
}

</script>

<style>
.container{
	background-color: #f8fffc;
	height: 100%;
}
.photo-icon{
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	margin-top: 10%;
}
.paizhao-secion{
	width: 80%;
	display: flex;
	flex-direction: column;
	align-items: center;
}
.paizhao-button,.ph-group{
	width: 240rpx;
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
.photo-text{
	margin-top: 60rpx;
	font-size: 32rpx;
	font-weight: 600;
}
.kouqiang-icon{
	height: 400rpx;
	width: 400rpx;
	background-color: white;
	border-radius: 50%;
	margin: 50rpx;
}
.camera-icon{
	width: 42rpx;
	height: 42rpx;
	border-radius: 50%;
	margin-right: 10rpx;
}

.ph-group{
	display: flex;
	justify-content: center;
	align-items: center;
}
.phone-text,.ph-text{
	margin-top: 18rpx;
	font-weight: bold;
	letter-spacing: 5rpx;
}
.ph-result-text{
	font-weight: bold;
	letter-spacing: 5rpx;
}

/* 图片部分 */
.ph-text{
	width: 80%;	
}
.photo-result{
	width: 100%;

	display: flex;
	flex-direction: column;
	align-items: center;
}
.button-group{
	display: flex;
	align-items: center;
	width: 100%;
	justify-content: center;
}
/* 确认图片 */
.confirm-button-container{
	width: 100%;
	display: flex;
	justify-content: center;
}
.restart-button{
	margin-right: 60rpx;
}

.confirm-button{
	display: flex;
	align-items: center;	justify-content: space-around;
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
	margin: 10rpx;
}



.button-group-down{
	width: 100%;
	margin-top: auto;
	display: flex;
	justify-content: center;
}
.photo-button{
	margin:30rpx;
}
.photo{
	display: flex;
	align-items: center;
	flex-direction: column;
	width: 100%;
}

.ph-container{
	display: flex;
	justify-content: center;
	margin-top: 36rpx;
}
.ph-result{
	display: flex;
	align-items: center;
	justify-content: center;
}

.ph-result-img{
	width: 48rpx;
	height: 48rpx;
	margin-right: 10rpx;
}


.picture-container{
	width: 90%;
	background-color: white;
	box-shadow: rgba(17, 17, 26, 0.05) 0px 1px 0px, rgba(17, 17, 26, 0.1) 0px 0px 8px;
	border-radius: 20rpx;
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 15rpx;
}
.photo-text{
	font-weight: bold;
	font-size: 42rpx;
	display: flex;
	margin-top: 12rpx;
	margin-bottom: 32rpx;
	margin-left: 24rpx;
	color: #162846;
}
.picture{
	width: 100%;
}


/* 健康状况 */
.advice{
	display: flex;
	flex-direction: column;
	align-items: start;
}
.yachi{
	margin: 20rpx;
	width: ;
}
.sport-list{
	display: flex;
	flex-direction: column;
}
.zhuangkuang{
	display: flex;
	justify-content: flex-start;
	align-items: center;
	font-size: 32rpx;
	font-family: sans-serif;
	font-weight: bold;
	color: #162846;
}
/* 健康方案 */
.fangan-title{
	font-family: sans-serif;
	font-weight: bold;
	color: #162846;
	display: flex;
	align-items: center;
	justify-content: flex-start;
	width: 100%;
	margin-bottom: 12rpx;
}
.advice-picture, .yachi-picture{
	width: 44rpx;
	height: 44rpx;
	margin: 20rpx;
}
.row1{
  font-family: sans-serif;
  font-weight: bold;
  color: #162846;
}

.zhuangkuang-container{
	display: flex;
	justify-content: center;
	margin-top: 20rpx;

}
.fangan-container{
	display: flex;
	justify-content: center;
	margin-top: 20rpx;
}
.health,.fangan-content{
  padding:20rpx;
  border-radius: 20rpx;
  background-color: white;
  display: flex;
  width: 90%;
  flex-direction: column;
	box-shadow: rgba(17, 17, 26, 0.05) 0px 1px 0px, rgba(17, 17, 26, 0.1) 0px 0px 8px;
}
.fangan-content{
	display: flex;
	justify-content: center;
}
.fu-title{
  font-family: sans-serif;
  font-weight: bold;
  font-size: 25rpx;
  color: #162846;
    margin-left: 16rpx;
}
.yinshi{
  margin-top: 10rpx;
  font-family: sans-serif;
  font-size: 24rpx;
  color: #7b7b7b;
  margin-left: 16rpx;
}
.fangan-item{
  display: flex;
  align-items: center;
  margin-bottom: 26rpx;
}
.text-section-1,.text-section-2{
  display: flex;
  padding:24rpx;
  background-color: #ffeeea;
  border-radius: 16rpx;
  align-items: center;
  font-size: 21rpx;
  color: rgb(225, 71, 71);
  width: 100%;
  font-weight: 600;
}
.text-section-2{
  color: rgb(91, 164, 241);
  background-color: #e0eaff;
}

.dot{
  width: 10rpx;
  height: 10rpx;
  content: "";
  background-color: rgb(225, 71, 71);
  display: flex;
  align-items: center;
  border-radius: 50%;
  margin-right: 18rpx;
}
.dot2{
  background-color: rgb(91, 164, 241);
}
.section-1{
  justify-self: flex-start;
}
.section-3{
  margin-left: auto;
}
.section-2{
  margin-left: 20%;
}
.tanxian{
  margin-left: 20%;
}


/* 加载页面 */
.loading-container{
	display: flex;
	flex-direction: column;
	align-items: center;
	height: 100%;
	justify-content: space-around;
	font-weight: bold;
	letter-spacing: 5rpx;
}
.loading {
  position: relative;
  width: 70px;
  height: 70px;
  border: 6px solid #000;
  border-top-color: rgba(0, 0, 0, 0.2);
  border-right-color: rgba(0, 0, 0, 0.2);
  border-bottom-color: rgba(0, 0, 0, 0.2);
  border-radius: 100%;

  animation: circle infinite 0.75s linear;
  margin: 30%;
}

@keyframes circle {
  0% {
    transform: rotate(0);
  }
  100% {
    transform: rotate(360deg);
  }
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
	letter-spacing: 5rpx;
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
</style>
			
