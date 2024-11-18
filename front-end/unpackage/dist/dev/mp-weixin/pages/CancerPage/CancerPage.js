"use strict";
const common_vendor = require("../../common/vendor.js");
const common_assets = require("../../common/assets.js");
const baseUrl = "http://192.168.225.36:5000/";
const _sfc_main = {
  __name: "CancerPage",
  setup(__props) {
    const bacColor = ["#c2e9fb", "#f5efef", "#d8fee1"];
    const textColor = ["#4481eb", "#ed6ea0", "#6fe186"];
    const analyseing = common_vendor.ref(false);
    const photoTaken = common_vendor.ref(true);
    const photoSelected = common_vendor.ref(false);
    const photoUrl = common_vendor.ref("");
    const photoName = common_vendor.ref("");
    const resData = common_vendor.reactive({
      analyse: [],
      problem: ""
    });
    function takeAPhoto() {
      console.log("开始请求");
      common_vendor.index.request({
        url: baseUrl + "prepare_cancer",
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
            photoUrl.value = baseUrl + `shot_cancer/${photoName.value}`;
            photoSelected.value = true;
          }, 3e3);
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
        url: baseUrl + `confirm_shot_cancer/${photoName.value}`,
        // 替换为您的实际API地址
        method: "GET",
        header: {
          "Content-Type": "application/json"
          // 设置请求头
        },
        success: (res) => {
          console.log(res);
          analyseing.value = false;
          resData.analyse = res.data.message.analyse;
          resData.problem = res.data.problem.message;
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
        d: common_assets._imports_0$1,
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
        w: common_assets._imports_4$1,
        x: common_assets._imports_5,
        y: common_vendor.f(resData.analyse, (item, k0, i0) => {
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
