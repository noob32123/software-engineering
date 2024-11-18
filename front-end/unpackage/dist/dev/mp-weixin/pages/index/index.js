"use strict";
const common_vendor = require("../../common/vendor.js");
const common_assets = require("../../common/assets.js");
const baseUrl = "http://192.168.225.36:5000/";
const _sfc_main = {
  __name: "index",
  setup(__props) {
    const bacColor = ["#c2e9fb", "#f5efef", "#d8fee1"];
    const textColor = ["#4481eb", "#ed6ea0", "#6fe186"];
    const analyseing = common_vendor.ref(false);
    const photoTaken = common_vendor.ref(true);
    const photoSelected = common_vendor.ref(false);
    const photoUrl = common_vendor.ref("nothing");
    const photoName = common_vendor.ref("");
    const resData = common_vendor.reactive({
      analyse: [],
      problem: ""
    });
    const showInfo = common_vendor.reactive({
      url: "../../static/quchi.jpg",
      text: "俗称蛀牙，指牙齿因细菌活动而造成分解的现象。常见的龋齿菌种是乳酸链球菌与转糖链球菌等革兰氏阳性好氧菌，它们代谢糖类后会产生能腐蚀牙齿的酸性物质。龋齿时会呈现黄色到黑色之间的不同颜色，其症状包含疼痛与进食困难，并发症包含牙齿周围组织发炎、牙齿丧失与形成牙齿脓肿。"
    });
    const staticInfo = [{
      name: "龋齿",
      url: "../../static/quchi.jpg",
      text: "俗称蛀牙，指牙齿因细菌活动而造成分解的现象。常见的龋齿菌种是乳酸链球菌与转糖链球菌等革兰氏阳性好氧菌，它们代谢糖类后会产生能腐蚀牙齿的酸性物质。龋齿时会呈现黄色到黑色之间的不同颜色，其症状包含疼痛与进食困难，并发症包含牙齿周围组织发炎、牙齿丧失与形成牙齿脓肿。"
    }, {
      name: "牙结石",
      url: "../../static/yajieshi.jpg",
      text: "一种坚硬的矿物质堆积物，当这些矿物质长期接触牙菌膜后，就会在牙齿表面形成牙结石。牙结石的其中一个征兆是牙齿根部出现粗糙不平的线条，但牙龈线下方亦有机会堆积牙结石。牙齿卫生员可以清除牙齿表面的形成的牙结石，良好的口腔护理则有助预防牙结石再次堆积。牙齿上没有被清除的牙菌膜会逐渐形成牙结石。牙菌膜由唾液、细菌、食物残渣和酸性物质所组成，当中的酸性物质由细菌结合含糖和淀粉类食物所产生；牙结石则是矿化的牙菌膜。牙结石主要包含矿化的已死细菌，以及唾液中少量矿化的蛋白质。"
    }, {
      name: "牙龈炎",
      url: "../../static/yayinyan.jpg",
      text: "牙齿附近的疾病之一。牙龈是牙周组织（牙龈、牙周膜、牙槽骨、牙骨质）之一，直接暴露于口腔中，直视可见，它是由角化上皮和结缔组织组成，覆盖着牙槽骨和牙根。牙龈病是局限于牙龈组织的病变，其中最为常见的是慢性龈缘炎，又称边缘性龈炎、单纯性龈炎，属于“仅与牙菌斑有关的牙龈炎”，是菌斑性牙龈炎中最常见的疾病。牙龈的炎症主要位于游离龈和龈乳头。"
    }, {
      name: "牙齿变色",
      url: "../../static/bianse.jpg",
      text: "正常牙齿为有光泽的黄白色，因身体和/或牙齿内改变所致的颜色或色泽的变化称为牙齿变色，又称为内源性牙齿着色。进入口腔的外来色素或口腔中细菌产生的色素在牙面沉积导致的牙齿着色称为牙齿外源性着色。"
    }, {
      name: "溃疡",
      url: "../../static/kuiyang.jpg",
      text: "又名“口疮”，是一种常见的口腔黏膜疾病，常出现在口腔内唇、上腭以及舌颊等部位黏膜上，形态呈圆形或椭圆形的疼痛溃疡点。多种因素如遗传、饮食、免疫力下降等可能诱发口腔溃疡的发展，具有很大的个体差异。我国约有10%～25%的人群患有复发性口腔溃疡，常见于10～30岁的群体中，女性患病率高于男性。"
    }, {
      name: "缺牙",
      url: "../../static/queya.jpg",
      text: "机体的营养、代谢、严重全身性疾患引起的疾病。指牙齿发育期间,在牙基质形成或基质钙化时,受到各种障碍造成牙齿发育的不正常,并且在牙体组织上留下永久性的缺陷或痕迹.常见的有:牙釉质发育不全,牙本质发育不全,氟斑牙和四环素染色牙。"
    }];
    function takeAPhoto() {
      console.log("开始请求");
      common_vendor.index.request({
        url: baseUrl + "prepare_teeth",
        // 替换为您的实际API地址
        method: "GET",
        header: {
          "Content-Type": "application/json"
          // 设置请求头
        },
        success: (res) => {
          photoName.value = res.data.message;
          console.log(photoName.value);
          setTimeout(function() {
            photoUrl.value = baseUrl + `shot_teeth/${photoName.value}`;
            photoSelected.value = true;
          }, 1e3);
        },
        fail: (err) => {
          console.error("请求失败", err);
        }
      });
    }
    function confirmPhoto() {
      console.log("确认图片");
      console.log(photoName.value);
      analyseing.value = true;
      common_vendor.index.request({
        url: baseUrl + `confirm_shot_teeth/${photoName.value}`,
        // 替换为您的实际API地址
        method: "GET",
        header: {
          "Content-Type": "application/json"
          // 设置请求头
        },
        success: (res) => {
          analyseing.value = false;
          console.log(res);
          resData.analyse = res.data.message.analyse;
          resData.problem = res.data.problem.message;
          for (let i = 0; i < 6; i++) {
            if (staticInfo[i].name === resData.problem) {
              showInfo.url = staticInfo[i].url;
              showInfo.text = staticInfo[i].text;
            }
          }
          photoTaken.value = true;
        },
        fail: (err) => {
          console.error("请求失败", err);
        }
      });
    }
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: !photoTaken.value
      }, !photoTaken.value ? common_vendor.e({
        b: "50px",
        c: !photoSelected.value
      }, !photoSelected.value ? {
        d: common_assets._imports_0,
        e: common_assets._imports_1,
        f: common_vendor.o(($event) => takeAPhoto())
      } : {}, {
        g: photoSelected.value && !analyseing.value
      }, photoSelected.value && !analyseing.value ? {
        h: photoUrl.value,
        i: common_assets._imports_1,
        j: common_vendor.o(($event) => takeAPhoto()),
        k: common_assets._imports_2,
        l: common_vendor.o(($event) => confirmPhoto())
      } : {}, {
        m: photoSelected.value && analyseing.value
      }, photoSelected.value && analyseing.value ? {} : {}) : {}, {
        n: photoTaken.value
      }, photoTaken.value ? {
        o: "30px",
        p: photoUrl.value,
        q: common_assets._imports_3,
        r: textColor[1],
        s: common_vendor.t(resData.problem),
        t: textColor[1],
        v: bacColor[1],
        w: showInfo.url,
        x: common_vendor.t(showInfo.text),
        y: common_assets._imports_5,
        z: common_vendor.f(resData.analyse, (item, k0, i0) => {
          return {
            a: common_vendor.t(item.title),
            b: common_vendor.f(item.content, (sen, k1, i1) => {
              return {
                a: common_vendor.t(sen)
              };
            })
          };
        })
      } : {});
    };
  }
};
wx.createPage(_sfc_main);
