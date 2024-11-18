<template>
	<scroll-view class="container" scroll-y="true">
		<!-- 拍摄部分 -->
		<view class="photo-section" v-if="!photoTaken">
			<view class="top-section" :style="{ paddingTop: 50 + 'px' }"></view>
			<view class="sum-title"></view>
			<view class="take-photo">
				<view class="photo-icon" v-if="!photoSelected && !photoing">
					<image class="kouqiang-icon" src="../../static/yachi.png"></image>
					<view class="paizhao-secion">
						<view class="paizhao-button" @click="takeAPhoto()">
							<image class="camera-icon" src="../../static/photo.png"></image>
							<view>上传图片</view>
						</view>
						<view class="phone-text">保证图片拍摄角度对准牙床。</view>
					</view>
				</view>
				
				<view class="loading1-container"  v-if="photoing">
					<div class="loading1">
						<div></div>
						<div></div>
						<div></div>
					</div>
					<view>正在上传文件</view>
				</view>
				
				<view class="photo-result" v-if="photoSelected&&!analyseing && !photoing">
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
					<view>正在分析牙齿健康状况..</view>
				</view>
				
			</view>
		</view>
		
		<!-- 拍摄结果分析部分 -->
		<view class="analyse-section" v-if="photoTaken">
			<view class="top-section" :style="{ paddingTop: 30 + 'px' }"></view>
			<view class="photo-text">口腔结果分析</view>
			
			<view class="photo">
				<view class="picture-container">
					<image class="picture" :src="photoUrl" mode="widthFix"></image>
				</view>
			</view>
			
			<view class="fangan-container">
				<view class="fangan-content">
					<view class="fangan-title">
					  <image
						src="../../static/advice.png"
						mode="scaleToFill"
						class="advice-picture"
					  />
					  检测结果
					</view>
					<view class="fangan-list">
						<view class="fangan-item">
							<view class="dot dot1" :style="{backgroundColor:textColor[1]}"></view>
							<view class="text-section-1" :style="{color:textColor[1],backgroundColor:bacColor[1]}">
								{{resData.problem}}
							</view>
						</view>
					</view>
					<view class="jieshao">
						<image class="disease-image" :src="showInfo.url"></image>
						<view class="jieshao-text">{{showInfo.text}}</view>
					</view>
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
						牙齿健康建议
					</view>
					<view class="content" v-for="item in resData.analyse">
						<view class="fu-title">{{item.title}}</view>
						<view class="yinshi">
							<view class="fu-content">{{item.content}}</view>
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
const analyseing=ref(false)
const photoTaken=ref(false)
const uploadpicname=ref("")
const photoSelected=ref(false)
const photoUrl=ref("nothing")
const photoName=ref("")
const baseUrl = "http://192.168.43.42:5173/"
const photoing = ref(false)
const resData=reactive({
	analyse:[],
	problem:""
})
const showInfo=reactive({
	url:"../../static/quchi.jpg",
	text:"俗称蛀牙，指牙齿因细菌活动而造成分解的现象。常见的龋齿菌种是乳酸链球菌与转糖链球菌等革兰氏阳性好氧菌，它们代谢糖类后会产生能腐蚀牙齿的酸性物质。龋齿时会呈现黄色到黑色之间的不同颜色，其症状包含疼痛与进食困难，并发症包含牙齿周围组织发炎、牙齿丧失与形成牙齿脓肿。"
})

const staticInfo=[{
	name:"龋齿",
	url:"../../static/quchi.jpg",
	text:"俗称蛀牙，指牙齿因细菌活动而造成分解的现象。常见的龋齿菌种是乳酸链球菌与转糖链球菌等革兰氏阳性好氧菌，它们代谢糖类后会产生能腐蚀牙齿的酸性物质。龋齿时会呈现黄色到黑色之间的不同颜色，其症状包含疼痛与进食困难，并发症包含牙齿周围组织发炎、牙齿丧失与形成牙齿脓肿。"
},{
	name:"牙结石",
	url:"../../static/yajieshi.jpg",
	text:"一种坚硬的矿物质堆积物，当这些矿物质长期接触牙菌膜后，就会在牙齿表面形成牙结石。牙结石的其中一个征兆是牙齿根部出现粗糙不平的线条，但牙龈线下方亦有机会堆积牙结石。牙齿卫生员可以清除牙齿表面的形成的牙结石，良好的口腔护理则有助预防牙结石再次堆积。牙齿上没有被清除的牙菌膜会逐渐形成牙结石。牙菌膜由唾液、细菌、食物残渣和酸性物质所组成，当中的酸性物质由细菌结合含糖和淀粉类食物所产生；牙结石则是矿化的牙菌膜。牙结石主要包含矿化的已死细菌，以及唾液中少量矿化的蛋白质。"
},{
	name:"牙龈炎",
	url:"../../static/yayinyan.jpg",
	text:"牙齿附近的疾病之一。牙龈是牙周组织（牙龈、牙周膜、牙槽骨、牙骨质）之一，直接暴露于口腔中，直视可见，它是由角化上皮和结缔组织组成，覆盖着牙槽骨和牙根。牙龈病是局限于牙龈组织的病变，其中最为常见的是慢性龈缘炎，又称边缘性龈炎、单纯性龈炎，属于“仅与牙菌斑有关的牙龈炎”，是菌斑性牙龈炎中最常见的疾病。牙龈的炎症主要位于游离龈和龈乳头。"
},{
	name:"牙齿变色",
	url:"../../static/bianse.jpg",
	text:"正常牙齿为有光泽的黄白色，因身体和/或牙齿内改变所致的颜色或色泽的变化称为牙齿变色，又称为内源性牙齿着色。进入口腔的外来色素或口腔中细菌产生的色素在牙面沉积导致的牙齿着色称为牙齿外源性着色。"
},{
	name:"溃疡",
	url:"../../static/kuiyang.jpg",
	text:"又名“口疮”，是一种常见的口腔黏膜疾病，常出现在口腔内唇、上腭以及舌颊等部位黏膜上，形态呈圆形或椭圆形的疼痛溃疡点。多种因素如遗传、饮食、免疫力下降等可能诱发口腔溃疡的发展，具有很大的个体差异。我国约有10%～25%的人群患有复发性口腔溃疡，常见于10～30岁的群体中，女性患病率高于男性。"
},{
	name:"牙齿结构异常",
	url:"../../static/queya.jpg",
	text:"机体的营养、代谢、严重全身性疾患引起的疾病。指牙齿发育期间,在牙基质形成或基质钙化时,受到各种障碍造成牙齿发育的不正常,并且在牙体组织上留下永久性的缺陷或痕迹.常见的有:牙釉质发育不全,牙本质发育不全,氟斑牙和四环素染色牙。"
}]

function takeAPhoto(){
	photoing.value=true;
	uni.chooseImage({
	    count: 1, // 选择一张图片
	    success: (res) => {
	        const filePath = res.tempFilePaths[0];
			console.log(filePath);
	        // 选择成功后调用上传接口
	        uni.uploadFile({
	            url: baseUrl+"getpictures_teeth",
	            filePath: filePath,
	            name: 'file',
	            success: (uploadFileRes) => {
	                console.log('上传成功:', uploadFileRes);
					uploadpicname.value=uploadFileRes.data;
					photoing.value=false;
					photoSelected.value=true;
					photoUrl.value=baseUrl+`shot_teeth/`+uploadpicname.value;
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
		url: baseUrl+`confirm_shot_teeth/`+uploadpicname.value, // 替换为您的实际API地址
		method: 'GET',
		header: {
			'Content-Type': 'application/json', // 设置请求头
		},
		success: (res) => {
			analyseing.value=false
			console.log(res)
			resData.analyse = res.data.message.analyse;
			resData.problem = res.data.problem.message
			for(let i=0;i<6;i++){
				if(staticInfo[i].name===resData.problem){
					showInfo.url=staticInfo[i].url
					showInfo.text=staticInfo[i].text
				}
			}
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
.phone-text{
	margin-top: 18rpx;
	font-weight: bold;
	letter-spacing: 5rpx;
}
/* 图片部分 */
.photo-result{
	width: 100%;
	display: flex;
	flex-direction: column;
	align-items: center;
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

.photo{
	display: flex;
	align-items: center;
	flex-direction: column;
	width: 100%;
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
.jieshao{
	width: 100%;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}
.disease-image{
	border-radius: 20rpx;
	box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
	margin-bottom: 10rpx;
}
.jieshao-text{
	margin-top: 10rpx;
	font-family: sans-serif;
	font-size: 24rpx;
	color: #7b7b7b;
	margin-left: 16rpx;
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
	margin-top: 60%;
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
			
