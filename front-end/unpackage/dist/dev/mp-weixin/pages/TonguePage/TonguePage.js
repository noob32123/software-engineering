"use strict";
const common_vendor = require("../../common/vendor.js");
const common_assets = require("../../common/assets.js");
const baseUrl = "http://192.168.225.36:5000/";
const _sfc_main = {
  __name: "TonguePage",
  setup(__props) {
    const bacColor = ["#c2e9fb", "#f5efef", "#d8fee1"];
    const textColor = ["#4481eb", "#ed6ea0", "#6fe186"];
    const photoTaken = common_vendor.ref(false);
    const photoSelected = common_vendor.ref(false);
    const phSelected = common_vendor.ref(false);
    const photoUrl = common_vendor.ref("nothing");
    const photoName = common_vendor.ref("");
    const resData = common_vendor.reactive({
      condition: [],
      analyse: []
    });
    const analyseing = common_vendor.ref(false);
    function takeAPhoto() {
      console.log("开始请求");
      common_vendor.index.request({
        url: baseUrl + "prepare_tongue",
        // 替换为您的实际API地址
        method: "GET",
        header: {
          "Content-Type": "application/json"
          // 设置请求头
        },
        success: (res) => {
          photoName.value = res.data.message;
          photoUrl.value = `${baseUrl}shot_tongue/${photoName.value}`;
          photoSelected.value = true;
        },
        fail: (err) => {
          console.error("请求失败", err);
        }
      });
    }
    function takeAPh() {
      setInterval(() => {
        phSelected.value = true;
      }, 2e3);
    }
    function confirmPhoto() {
      console.log("确认图片");
      analyseing.value = true;
      common_vendor.index.request({
        url: baseUrl + "confirm_shot_tongue/" + photoName.value,
        // 替换为您的实际API地址
        method: "GET",
        header: {
          "Content-Type": "application/json"
          // 设置请求头
        },
        success: (res) => {
          analyseing.value = false;
          console.log(res);
          resData.condition = res.data.message.condition;
          resData.analyse = res.data.message.analyse;
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
      }, photoSelected.value && analyseing.value ? {} : {}, {
        n: !analyseing.value
      }, !analyseing.value ? common_vendor.e({
        o: !phSelected.value
      }, !phSelected.value ? {
        p: common_assets._imports_3$1,
        q: common_vendor.o(($event) => takeAPh())
      } : {}, {
        r: phSelected.value
      }, phSelected.value ? {
        s: common_assets._imports_4
      } : {}) : {}) : {}, {
        t: photoTaken.value
      }, photoTaken.value ? {
        v: "30px",
        w: photoUrl.value,
        x: common_assets._imports_5,
        y: common_vendor.f(resData.condition, (item, k0, i0) => {
          return {
            a: common_vendor.t(item.title),
            b: common_vendor.f(item.content, (sen, k1, i1) => {
              return {
                a: common_vendor.t(sen)
              };
            })
          };
        }),
        z: common_assets._imports_3,
        A: common_vendor.f(resData.analyse, (item, k0, i0) => {
          return {
            a: common_vendor.f(item.content, (sentence, index, i1) => {
              return {
                a: textColor[index % 3],
                b: common_vendor.t(sentence),
                c: textColor[index % 3],
                d: bacColor[index % 3]
              };
            })
          };
        })
      } : {});
    };
  }
};
wx.createPage(_sfc_main);
