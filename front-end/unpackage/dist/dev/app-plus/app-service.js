if (typeof Promise !== "undefined" && !Promise.prototype.finally) {
  Promise.prototype.finally = function(callback) {
    const promise = this.constructor;
    return this.then(
      (value) => promise.resolve(callback()).then(() => value),
      (reason) => promise.resolve(callback()).then(() => {
        throw reason;
      })
    );
  };
}
;
if (typeof uni !== "undefined" && uni && uni.requireGlobal) {
  const global = uni.requireGlobal();
  ArrayBuffer = global.ArrayBuffer;
  Int8Array = global.Int8Array;
  Uint8Array = global.Uint8Array;
  Uint8ClampedArray = global.Uint8ClampedArray;
  Int16Array = global.Int16Array;
  Uint16Array = global.Uint16Array;
  Int32Array = global.Int32Array;
  Uint32Array = global.Uint32Array;
  Float32Array = global.Float32Array;
  Float64Array = global.Float64Array;
  BigInt64Array = global.BigInt64Array;
  BigUint64Array = global.BigUint64Array;
}
;
if (uni.restoreGlobal) {
  uni.restoreGlobal(Vue, weex, plus, setTimeout, clearTimeout, setInterval, clearInterval);
}
(function(vue) {
  "use strict";
  function formatAppLog(type, filename, ...args) {
    if (uni.__log__) {
      uni.__log__(type, filename, ...args);
    } else {
      console[type].apply(console, [...args, filename]);
    }
  }
  const _imports_0$2 = "/static/yachi.png";
  const _imports_2$1 = "/static/photo.png";
  const _imports_2 = "/static/yes.png";
  const _imports_3$2 = "/static/advice.png";
  const _imports_5$1 = "/static/oral.png";
  const _export_sfc = (sfc, props) => {
    const target = sfc.__vccOpts || sfc;
    for (const [key, val] of props) {
      target[key] = val;
    }
    return target;
  };
  const baseUrl$3 = "http://192.168.234.36:5000/";
  const _sfc_main$4 = {
    __name: "index",
    setup(__props) {
      const bacColor = ["#c2e9fb", "#f5efef", "#d8fee1"];
      const textColor = ["#4481eb", "#ed6ea0", "#6fe186"];
      const analyseing = vue.ref(false);
      const photoTaken = vue.ref(false);
      const photoSelected = vue.ref(false);
      const photoUrl = vue.ref("nothing");
      const photoName = vue.ref("");
      const photoing = vue.ref(false);
      const resData = vue.reactive({
        analyse: [],
        problem: ""
      });
      const showInfo = vue.reactive({
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
        name: "牙齿结构异常",
        url: "../../static/queya.jpg",
        text: "机体的营养、代谢、严重全身性疾患引起的疾病。指牙齿发育期间,在牙基质形成或基质钙化时,受到各种障碍造成牙齿发育的不正常,并且在牙体组织上留下永久性的缺陷或痕迹.常见的有:牙釉质发育不全,牙本质发育不全,氟斑牙和四环素染色牙。"
      }];
      function takeAPhoto() {
        formatAppLog("log", "at pages/index/index.vue:162", "开始请求");
        photoing.value = true;
        uni.request({
          url: baseUrl$3 + "prepare_teeth",
          method: "GET",
          header: {
            "Content-Type": "application/json"
          },
          success: (res) => {
            photoName.value = res.data.message;
            formatAppLog("log", "at pages/index/index.vue:173", photoName.value);
            photoUrl.value = baseUrl$3 + `shot_teeth/${photoName.value}`;
            photoSelected.value = true;
            photoing.value = false;
          },
          fail: (err) => {
            formatAppLog("error", "at pages/index/index.vue:179", "请求失败", err);
          }
        });
      }
      function confirmPhoto() {
        formatAppLog("log", "at pages/index/index.vue:185", "确认图片");
        formatAppLog("log", "at pages/index/index.vue:186", photoName.value);
        analyseing.value = true;
        uni.request({
          url: baseUrl$3 + `confirm_shot_teeth/${photoName.value}`,
          // 替换为您的实际API地址
          method: "GET",
          header: {
            "Content-Type": "application/json"
            // 设置请求头
          },
          success: (res) => {
            analyseing.value = false;
            formatAppLog("log", "at pages/index/index.vue:196", res);
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
            formatAppLog("error", "at pages/index/index.vue:208", "请求失败", err);
          }
        });
      }
      return (_ctx, _cache) => {
        return vue.openBlock(), vue.createElementBlock("scroll-view", {
          class: "container",
          "scroll-y": "true"
        }, [
          vue.createCommentVNode(" 拍摄部分 "),
          !photoTaken.value ? (vue.openBlock(), vue.createElementBlock("view", {
            key: 0,
            class: "photo-section"
          }, [
            vue.createElementVNode("view", {
              class: "top-section",
              style: { paddingTop: "50px" }
            }),
            vue.createElementVNode("view", { class: "sum-title" }),
            vue.createElementVNode("view", { class: "take-photo" }, [
              !photoSelected.value && !photoing.value ? (vue.openBlock(), vue.createElementBlock("view", {
                key: 0,
                class: "photo-icon"
              }, [
                vue.createElementVNode("image", {
                  class: "kouqiang-icon",
                  src: _imports_0$2
                }),
                vue.createElementVNode("view", { class: "paizhao-secion" }, [
                  vue.createElementVNode("view", {
                    class: "paizhao-button",
                    onClick: _cache[0] || (_cache[0] = ($event) => takeAPhoto())
                  }, [
                    vue.createElementVNode("image", {
                      class: "camera-icon",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "开始拍照")
                  ]),
                  vue.createElementVNode("view", { class: "phone-text" }, "请将摄像头按照对准牙床，确保拍摄角度与上图一致。")
                ])
              ])) : vue.createCommentVNode("v-if", true),
              photoing.value ? (vue.openBlock(), vue.createElementBlock("view", {
                key: 1,
                class: "loading1-container"
              }, [
                vue.createElementVNode("div", { class: "loading1" }, [
                  vue.createElementVNode("div"),
                  vue.createElementVNode("div"),
                  vue.createElementVNode("div")
                ]),
                vue.createElementVNode("view", null, "正在调用拍摄模块...")
              ])) : vue.createCommentVNode("v-if", true),
              photoSelected.value && !analyseing.value && !photoing.value ? (vue.openBlock(), vue.createElementBlock("view", {
                key: 2,
                class: "photo-result"
              }, [
                vue.createElementVNode("image", {
                  src: photoUrl.value,
                  mode: "scaleToFill",
                  class: "yachi"
                }, null, 8, ["src"]),
                vue.createElementVNode("view", { class: "confirm-button-container" }, [
                  vue.createElementVNode("view", {
                    class: "restart-button confirm-button",
                    onClick: _cache[1] || (_cache[1] = ($event) => takeAPhoto())
                  }, [
                    vue.createElementVNode("image", {
                      class: "yes",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "重新拍摄")
                  ]),
                  vue.createElementVNode("view", {
                    class: "confirm-button",
                    onClick: _cache[2] || (_cache[2] = ($event) => confirmPhoto())
                  }, [
                    vue.createElementVNode("image", {
                      class: "yes",
                      src: _imports_2
                    }),
                    vue.createElementVNode("view", null, "确认图片")
                  ])
                ])
              ])) : vue.createCommentVNode("v-if", true),
              photoSelected.value && analyseing.value ? (vue.openBlock(), vue.createElementBlock("view", {
                key: 3,
                class: "loading-container"
              }, [
                vue.createElementVNode("div", { class: "loading" }),
                vue.createElementVNode("view", null, "正在分析牙齿健康状况..")
              ])) : vue.createCommentVNode("v-if", true)
            ])
          ])) : vue.createCommentVNode("v-if", true),
          vue.createCommentVNode(" 拍摄结果分析部分 "),
          photoTaken.value ? (vue.openBlock(), vue.createElementBlock("view", {
            key: 1,
            class: "analyse-section"
          }, [
            vue.createElementVNode("view", {
              class: "top-section",
              style: { paddingTop: "30px" }
            }),
            vue.createElementVNode("view", { class: "photo-text" }, "口腔结果分析"),
            vue.createElementVNode("view", { class: "photo" }, [
              vue.createElementVNode("view", { class: "picture-container" }, [
                vue.createElementVNode("image", {
                  class: "picture",
                  src: photoUrl.value,
                  mode: "widthFix"
                }, null, 8, ["src"])
              ])
            ]),
            vue.createElementVNode("view", { class: "fangan-container" }, [
              vue.createElementVNode("view", { class: "fangan-content" }, [
                vue.createElementVNode("view", { class: "fangan-title" }, [
                  vue.createElementVNode("image", {
                    src: _imports_3$2,
                    mode: "scaleToFill",
                    class: "advice-picture"
                  }),
                  vue.createTextVNode(" 检测结果 ")
                ]),
                vue.createElementVNode("view", { class: "fangan-list" }, [
                  vue.createElementVNode("view", { class: "fangan-item" }, [
                    vue.createElementVNode(
                      "view",
                      {
                        class: "dot dot1",
                        style: vue.normalizeStyle({ backgroundColor: textColor[1] })
                      },
                      null,
                      4
                      /* STYLE */
                    ),
                    vue.createElementVNode(
                      "view",
                      {
                        class: "text-section-1",
                        style: vue.normalizeStyle({ color: textColor[1], backgroundColor: bacColor[1] })
                      },
                      vue.toDisplayString(resData.problem),
                      5
                      /* TEXT, STYLE */
                    )
                  ])
                ]),
                vue.createElementVNode("view", { class: "jieshao" }, [
                  vue.createElementVNode("image", {
                    class: "disease-image",
                    src: showInfo.url
                  }, null, 8, ["src"]),
                  vue.createElementVNode(
                    "view",
                    { class: "jieshao-text" },
                    vue.toDisplayString(showInfo.text),
                    1
                    /* TEXT */
                  )
                ])
              ])
            ]),
            vue.createElementVNode("view", { class: "zhuangkuang-container" }, [
              vue.createElementVNode("view", { class: "health" }, [
                vue.createElementVNode("view", { class: "zhuangkuang" }, [
                  vue.createElementVNode("image", {
                    src: _imports_5$1,
                    mode: "scaleToFill",
                    class: "yachi-picture"
                  }),
                  vue.createTextVNode(" 牙齿健康建议 ")
                ]),
                (vue.openBlock(true), vue.createElementBlock(
                  vue.Fragment,
                  null,
                  vue.renderList(resData.analyse, (item) => {
                    return vue.openBlock(), vue.createElementBlock("view", { class: "content" }, [
                      vue.createElementVNode(
                        "view",
                        { class: "fu-title" },
                        vue.toDisplayString(item.title),
                        1
                        /* TEXT */
                      ),
                      vue.createElementVNode("view", { class: "yinshi" }, [
                        vue.createElementVNode(
                          "view",
                          { class: "fu-content" },
                          vue.toDisplayString(item.content),
                          1
                          /* TEXT */
                        )
                      ])
                    ]);
                  }),
                  256
                  /* UNKEYED_FRAGMENT */
                ))
              ])
            ])
          ])) : vue.createCommentVNode("v-if", true)
        ]);
      };
    }
  };
  const PagesIndexIndex = /* @__PURE__ */ _export_sfc(_sfc_main$4, [["__file", "G:/projects/uniapp/iot-front/pages/index/index.vue"]]);
  const _imports_0$1 = "/static/shetou.png";
  const _imports_3$1 = "/static/ph.png";
  const _imports_4$2 = "/static/ph-result.png";
  const _imports_6$1 = "/static/digest.png";
  const baseUrl$2 = "http://192.168.234.36:5000/";
  const _sfc_main$3 = {
    __name: "TonguePage",
    setup(__props) {
      const bacColor = ["#c2e9fb", "#f5efef", "#d8fee1"];
      const textColor = ["#4481eb", "#ed6ea0", "#6fe186"];
      const photoTaken = vue.ref(false);
      const photoSelected = vue.ref(false);
      const phSelected = vue.ref(false);
      const photoUrl = vue.ref("nothing");
      const photoName = vue.ref("");
      const resData = vue.reactive({
        condition: [],
        analyse: []
      });
      const analyseing = vue.ref(false);
      const photoing = vue.ref(false);
      const ph = vue.ref("");
      function takeAPhoto() {
        photoing.value = true;
        formatAppLog("log", "at pages/TonguePage/TonguePage.vue:169", "开始请求");
        uni.request({
          url: baseUrl$2 + "prepare_tongue",
          method: "GET",
          header: {
            "Content-Type": "application/json"
          },
          success: (res) => {
            photoing.value = false;
            photoName.value = res.data.message;
            photoUrl.value = `${baseUrl$2}shot_tongue/${photoName.value}`;
            photoSelected.value = true;
          },
          fail: (err) => {
            formatAppLog("error", "at pages/TonguePage/TonguePage.vue:183", "请求失败", err);
          }
        });
      }
      function takeAPh() {
        formatAppLog("log", "at pages/TonguePage/TonguePage.vue:189", "take a ph");
        uni.request({
          url: baseUrl$2 + "phtest",
          method: "GET",
          header: {
            "Content-Type": "application/json"
          },
          success: (res) => {
            formatAppLog("log", "at pages/TonguePage/TonguePage.vue:197", "ph调用成功");
            formatAppLog("log", "at pages/TonguePage/TonguePage.vue:198", res);
            ph.value = res.data.message;
            phSelected.value = true;
          },
          fail: (err) => {
            formatAppLog("error", "at pages/TonguePage/TonguePage.vue:203", "请求失败", err);
          }
        });
      }
      function confirmPhoto() {
        formatAppLog("log", "at pages/TonguePage/TonguePage.vue:209", "确认图片");
        analyseing.value = true;
        uni.request({
          url: baseUrl$2 + "confirm_shot_tongue/" + photoName.value,
          // 替换为您的实际API地址
          method: "GET",
          header: {
            "Content-Type": "application/json"
            // 设置请求头
          },
          success: (res) => {
            analyseing.value = false;
            formatAppLog("log", "at pages/TonguePage/TonguePage.vue:219", res);
            resData.condition = res.data.message.condition;
            resData.analyse = res.data.message.analyse;
            photoTaken.value = true;
          },
          fail: (err) => {
            formatAppLog("error", "at pages/TonguePage/TonguePage.vue:225", "请求失败", err);
          }
        });
      }
      return (_ctx, _cache) => {
        return vue.openBlock(), vue.createElementBlock("scroll-view", {
          class: "container",
          "scroll-y": "true"
        }, [
          vue.createCommentVNode(" 拍摄部分 "),
          !photoTaken.value ? (vue.openBlock(), vue.createElementBlock("view", {
            key: 0,
            class: "photo-section"
          }, [
            vue.createCommentVNode(" 拍照 "),
            vue.createElementVNode("view", {
              class: "top-section",
              style: { paddingTop: "50px" }
            }),
            vue.createElementVNode("view", { class: "take-photo" }, [
              !photoSelected.value && !photoing.value ? (vue.openBlock(), vue.createElementBlock("view", {
                key: 0,
                class: "photo-icon"
              }, [
                vue.createElementVNode("image", {
                  class: "kouqiang-icon",
                  src: _imports_0$1
                }),
                vue.createElementVNode("view", { class: "paizhao-secion" }, [
                  vue.createElementVNode("view", {
                    class: "paizhao-button",
                    onClick: _cache[0] || (_cache[0] = ($event) => takeAPhoto())
                  }, [
                    vue.createElementVNode("image", {
                      class: "camera-icon",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "开始拍照")
                  ]),
                  vue.createElementVNode("view", { class: "phone-text" }, "请将摄像头按照对准舌苔，确保拍摄角度与上图一致。")
                ])
              ])) : vue.createCommentVNode("v-if", true),
              photoing.value ? (vue.openBlock(), vue.createElementBlock("view", {
                key: 1,
                class: "loading1-container"
              }, [
                vue.createElementVNode("div", { class: "loading1" }, [
                  vue.createElementVNode("div"),
                  vue.createElementVNode("div"),
                  vue.createElementVNode("div")
                ]),
                vue.createElementVNode("view", null, "正在调用拍摄模块...")
              ])) : vue.createCommentVNode("v-if", true),
              photoSelected.value && !analyseing.value && !photoing.value ? (vue.openBlock(), vue.createElementBlock("view", {
                key: 2,
                class: "photo-result"
              }, [
                vue.createElementVNode("image", {
                  src: photoUrl.value,
                  mode: "scaleToFill",
                  class: "yachi"
                }, null, 8, ["src"]),
                vue.createElementVNode("view", { class: "confirm-button-container" }, [
                  vue.createElementVNode("view", {
                    class: "restart-button confirm-button",
                    onClick: _cache[1] || (_cache[1] = ($event) => takeAPhoto())
                  }, [
                    vue.createElementVNode("image", {
                      class: "yes",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "重新拍摄")
                  ]),
                  vue.createElementVNode("view", {
                    class: "confirm-button",
                    onClick: _cache[2] || (_cache[2] = ($event) => confirmPhoto())
                  }, [
                    vue.createElementVNode("image", {
                      class: "yes",
                      src: _imports_2
                    }),
                    vue.createElementVNode("view", null, "确认图片")
                  ])
                ])
              ])) : vue.createCommentVNode("v-if", true),
              photoSelected.value && analyseing.value ? (vue.openBlock(), vue.createElementBlock("view", {
                key: 3,
                class: "loading-container"
              }, [
                vue.createElementVNode("div", { class: "loading" }),
                vue.createElementVNode("view", null, "正在分析消化健康状况...")
              ])) : vue.createCommentVNode("v-if", true)
            ]),
            vue.createCommentVNode(" ph "),
            !analyseing.value ? (vue.openBlock(), vue.createElementBlock("view", {
              key: 0,
              class: "take-photo"
            }, [
              !phSelected.value ? (vue.openBlock(), vue.createElementBlock("view", {
                key: 0,
                class: "photo-icon"
              }, [
                vue.createElementVNode("view", {
                  class: "ph-group",
                  onClick: _cache[3] || (_cache[3] = ($event) => takeAPh())
                }, [
                  vue.createElementVNode("image", {
                    class: "camera-icon",
                    src: _imports_3$1
                  }),
                  vue.createElementVNode("view", null, "开始检测")
                ]),
                vue.createElementVNode("view", { class: "ph-text" }, "请将ph检测探头放入待检测液中，并点击ph检测按钮进行检测（可选）")
              ])) : vue.createCommentVNode("v-if", true),
              vue.createElementVNode("view", { class: "ph-container" }, [
                phSelected.value ? (vue.openBlock(), vue.createElementBlock("view", {
                  key: 0,
                  class: "ph-result"
                }, [
                  vue.createElementVNode("image", {
                    class: "ph-result-img",
                    src: _imports_4$2
                  }),
                  vue.createElementVNode(
                    "view",
                    { class: "ph-result-text" },
                    "PH检测结果:" + vue.toDisplayString(ph.value),
                    1
                    /* TEXT */
                  )
                ])) : vue.createCommentVNode("v-if", true)
              ])
            ])) : vue.createCommentVNode("v-if", true)
          ])) : vue.createCommentVNode("v-if", true),
          vue.createCommentVNode(" 拍摄结果分析部分 "),
          photoTaken.value ? (vue.openBlock(), vue.createElementBlock("view", {
            key: 1,
            class: "analyse-section"
          }, [
            vue.createElementVNode("view", {
              class: "top-section",
              style: { paddingTop: "30px" }
            }),
            vue.createElementVNode("view", { class: "photo-text" }, "舌苔结果分析"),
            vue.createElementVNode("view", { class: "photo" }, [
              vue.createElementVNode("view", { class: "picture-container" }, [
                vue.createElementVNode("image", {
                  class: "picture",
                  src: photoUrl.value,
                  mode: "widthFix"
                }, null, 8, ["src"])
              ])
            ]),
            vue.createElementVNode("view", { class: "zhuangkuang-container" }, [
              vue.createElementVNode("view", { class: "health" }, [
                vue.createElementVNode("view", { class: "zhuangkuang" }, [
                  vue.createElementVNode("image", {
                    src: _imports_5$1,
                    mode: "scaleToFill",
                    class: "yachi-picture"
                  }),
                  vue.createTextVNode(" 舌苔健康状况 ")
                ]),
                (vue.openBlock(true), vue.createElementBlock(
                  vue.Fragment,
                  null,
                  vue.renderList(resData.condition, (item) => {
                    return vue.openBlock(), vue.createElementBlock("view", { class: "content" }, [
                      vue.createElementVNode(
                        "view",
                        { class: "fu-title" },
                        vue.toDisplayString(item.title),
                        1
                        /* TEXT */
                      ),
                      vue.createElementVNode("view", { class: "yinshi" }, [
                        (vue.openBlock(true), vue.createElementBlock(
                          vue.Fragment,
                          null,
                          vue.renderList(item.content, (sen) => {
                            return vue.openBlock(), vue.createElementBlock(
                              "view",
                              { class: "fu-content" },
                              vue.toDisplayString(sen),
                              1
                              /* TEXT */
                            );
                          }),
                          256
                          /* UNKEYED_FRAGMENT */
                        ))
                      ])
                    ]);
                  }),
                  256
                  /* UNKEYED_FRAGMENT */
                ))
              ])
            ]),
            vue.createElementVNode("view", { class: "zhuangkuang-container" }, [
              vue.createElementVNode("view", { class: "health" }, [
                vue.createElementVNode("view", { class: "zhuangkuang" }, [
                  vue.createElementVNode("image", {
                    src: _imports_6$1,
                    mode: "scaleToFill",
                    class: "yachi-picture"
                  }),
                  vue.createTextVNode(" ph检测分析 ")
                ]),
                vue.createElementVNode("view", { class: "content" }, [
                  vue.createElementVNode("view", { class: "yinshi" }, [
                    vue.createElementVNode("view", { class: "fu-content" }, "口腔pH值为6.86,正常口腔PH值范围为6.6-7.0，因此您的口腔PH值在正常范围内。")
                  ])
                ])
              ])
            ]),
            vue.createElementVNode("view", { class: "fangan-container" }, [
              vue.createElementVNode("view", { class: "fangan-content" }, [
                vue.createElementVNode("view", { class: "fangan-title" }, [
                  vue.createElementVNode("image", {
                    src: _imports_3$2,
                    mode: "scaleToFill",
                    class: "advice-picture"
                  }),
                  vue.createTextVNode(" 护理建议 ")
                ]),
                (vue.openBlock(true), vue.createElementBlock(
                  vue.Fragment,
                  null,
                  vue.renderList(resData.analyse, (item) => {
                    return vue.openBlock(), vue.createElementBlock("view", { class: "fangan-list" }, [
                      (vue.openBlock(true), vue.createElementBlock(
                        vue.Fragment,
                        null,
                        vue.renderList(item.content, (sentence, index) => {
                          return vue.openBlock(), vue.createElementBlock("view", { class: "fangan-item" }, [
                            vue.createElementVNode(
                              "view",
                              {
                                class: "dot dot1",
                                style: vue.normalizeStyle({ backgroundColor: textColor[index % 3] })
                              },
                              null,
                              4
                              /* STYLE */
                            ),
                            vue.createElementVNode(
                              "view",
                              {
                                class: "text-section-1",
                                style: vue.normalizeStyle({ color: textColor[index % 3], backgroundColor: bacColor[index % 3] })
                              },
                              vue.toDisplayString(sentence),
                              5
                              /* TEXT, STYLE */
                            )
                          ]);
                        }),
                        256
                        /* UNKEYED_FRAGMENT */
                      ))
                    ]);
                  }),
                  256
                  /* UNKEYED_FRAGMENT */
                ))
              ])
            ])
          ])) : vue.createCommentVNode("v-if", true)
        ]);
      };
    }
  };
  const PagesTonguePageTonguePage = /* @__PURE__ */ _export_sfc(_sfc_main$3, [["__file", "G:/projects/uniapp/iot-front/pages/TonguePage/TonguePage.vue"]]);
  const _imports_4$1 = "/static/cancer-zhengzhuang.jpg";
  const baseUrl$1 = "http://192.168.234.36:5000/";
  const _sfc_main$2 = {
    __name: "CancerPage",
    setup(__props) {
      const bacColor = ["#c2e9fb", "#f5efef", "#d8fee1"];
      const textColor = ["#4481eb", "#ed6ea0", "#6fe186"];
      const rick = vue.reactive({
        bac: "#c2e9fb",
        text: "#4481eb"
      });
      const analyseing = vue.ref(false);
      const photoTaken = vue.ref(false);
      const photoSelected = vue.ref(false);
      const photoUrl = vue.ref("");
      const photoName = vue.ref("");
      const resData = vue.reactive({
        analyse: [],
        problem: ""
      });
      const photoing = vue.ref(false);
      function takeAPhoto() {
        formatAppLog("log", "at pages/CancerPage/CancerPage.vue:137", "开始请求");
        photoing.value = true;
        uni.request({
          url: baseUrl$1 + "prepare_cancer",
          // 替换为您的实际API地址
          method: "GET",
          header: {
            "Content-Type": "application/json"
          },
          success: (res) => {
            photoing.value = false;
            photoName.value = res.data.message;
            formatAppLog("log", "at pages/CancerPage/CancerPage.vue:149", photoName.value);
            photoUrl.value = baseUrl$1 + `shot_cancer/${photoName.value}`;
            photoSelected.value = true;
          },
          fail: (err) => {
            formatAppLog("error", "at pages/CancerPage/CancerPage.vue:154", "请求失败", err);
          }
        });
      }
      function confirmPhoto() {
        formatAppLog("log", "at pages/CancerPage/CancerPage.vue:160", "确认图片");
        formatAppLog("log", "at pages/CancerPage/CancerPage.vue:161", photoName.value);
        analyseing.value = true;
        uni.request({
          url: baseUrl$1 + `confirm_shot_cancer/${photoName.value}`,
          // 替换为您的实际API地址
          method: "GET",
          header: {
            "Content-Type": "application/json"
            // 设置请求头
          },
          success: (res) => {
            formatAppLog("log", "at pages/CancerPage/CancerPage.vue:170", res);
            analyseing.value = false;
            resData.analyse = res.data.message.analyse;
            resData.problem = res.data.problem.message;
            if (resData.problem === "已得口腔癌" || resData.problem === "有高风险得口腔癌") {
              rick.bac = bacColor[1];
              rick.text = textColor[1];
            }
            if (resData.problem === "有低风险得口腔癌" || resData.problem === "口腔有溃疡") {
              rick.bac = bacColor[0];
              rick.text = textColor[0];
            }
            if (resData.problem === "口腔状态正常") {
              rick.bac = bacColor[2];
              rick.text = textColor[2];
            }
            photoTaken.value = true;
          },
          fail: (err) => {
            formatAppLog("error", "at pages/CancerPage/CancerPage.vue:189", "请求失败", err);
          }
        });
      }
      return (_ctx, _cache) => {
        return vue.openBlock(), vue.createElementBlock("scroll-view", {
          class: "container",
          "scroll-y": "true"
        }, [
          vue.createCommentVNode(" 拍摄部分 "),
          !photoTaken.value ? (vue.openBlock(), vue.createElementBlock("view", {
            key: 0,
            class: "photo-section"
          }, [
            vue.createElementVNode("view", {
              class: "top-section",
              style: { paddingTop: "50px" }
            }),
            vue.createElementVNode("view", { class: "take-photo" }, [
              !photoSelected.value && !photoing.value ? (vue.openBlock(), vue.createElementBlock("view", {
                key: 0,
                class: "photo-icon"
              }, [
                vue.createElementVNode("image", {
                  class: "kouqiang-icon",
                  src: _imports_0$1
                }),
                vue.createElementVNode("view", { class: "paizhao-secion" }, [
                  vue.createElementVNode("view", {
                    class: "paizhao-button",
                    onClick: _cache[0] || (_cache[0] = ($event) => takeAPhoto())
                  }, [
                    vue.createElementVNode("image", {
                      class: "camera-icon",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "开始拍照")
                  ]),
                  vue.createElementVNode("view", { class: "phone-text" }, "请将摄像头按照对准口腔，确保拍摄角度与上图一致。")
                ])
              ])) : vue.createCommentVNode("v-if", true),
              photoing.value ? (vue.openBlock(), vue.createElementBlock("view", {
                key: 1,
                class: "loading1-container"
              }, [
                vue.createElementVNode("div", { class: "loading1" }, [
                  vue.createElementVNode("div"),
                  vue.createElementVNode("div"),
                  vue.createElementVNode("div")
                ]),
                vue.createElementVNode("view", null, "正在调用拍摄模块...")
              ])) : vue.createCommentVNode("v-if", true),
              photoSelected.value && !analyseing.value && !photoing.value ? (vue.openBlock(), vue.createElementBlock("view", {
                key: 2,
                class: "photo-result"
              }, [
                vue.createElementVNode("image", {
                  src: photoUrl.value,
                  mode: "scaleToFill",
                  class: "yachi"
                }, null, 8, ["src"]),
                vue.createElementVNode("view", { class: "confirm-button-container" }, [
                  vue.createElementVNode("view", {
                    class: "restart-button confirm-button",
                    onClick: _cache[1] || (_cache[1] = ($event) => takeAPhoto())
                  }, [
                    vue.createElementVNode("image", {
                      class: "yes",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "重新拍摄")
                  ]),
                  vue.createElementVNode("view", {
                    class: "confirm-button",
                    onClick: _cache[2] || (_cache[2] = ($event) => confirmPhoto())
                  }, [
                    vue.createElementVNode("image", {
                      class: "yes",
                      src: _imports_2
                    }),
                    vue.createElementVNode("view", null, "确认图片")
                  ])
                ])
              ])) : vue.createCommentVNode("v-if", true),
              photoSelected.value && analyseing.value ? (vue.openBlock(), vue.createElementBlock("view", {
                key: 3,
                class: "loading-container"
              }, [
                vue.createElementVNode("div", { class: "loading" }),
                vue.createElementVNode("view", null, "正在分析口腔癌风险...")
              ])) : vue.createCommentVNode("v-if", true)
            ])
          ])) : vue.createCommentVNode("v-if", true),
          vue.createCommentVNode(" 拍摄结果分析部分 "),
          photoTaken.value ? (vue.openBlock(), vue.createElementBlock("view", {
            key: 1,
            class: "analyse-section"
          }, [
            vue.createElementVNode("view", {
              class: "top-section",
              style: { paddingTop: "30px" }
            }),
            vue.createElementVNode("view", { class: "photo-text" }, "口腔癌风险监测"),
            vue.createElementVNode("view", { class: "photo" }, [
              vue.createElementVNode("view", { class: "picture-container" }, [
                vue.createElementVNode("image", {
                  class: "picture",
                  src: photoUrl.value,
                  mode: "widthFix"
                }, null, 8, ["src"])
              ])
            ]),
            vue.createElementVNode("view", { class: "fangan-container" }, [
              vue.createElementVNode("view", { class: "fangan-content" }, [
                vue.createElementVNode("view", { class: "fangan-title" }, [
                  vue.createElementVNode("image", {
                    src: _imports_3$2,
                    mode: "scaleToFill",
                    class: "advice-picture"
                  }),
                  vue.createTextVNode(" 监测结果 ")
                ]),
                vue.createElementVNode("view", { class: "fangan-list" }, [
                  vue.createElementVNode("view", { class: "fangan-item" }, [
                    vue.createElementVNode(
                      "view",
                      {
                        class: "dot dot1",
                        style: vue.normalizeStyle({ backgroundColor: rick.text })
                      },
                      null,
                      4
                      /* STYLE */
                    ),
                    vue.createElementVNode(
                      "view",
                      {
                        class: "text-section-1",
                        style: vue.normalizeStyle({ color: rick.text, backgroundColor: rick.bac })
                      },
                      vue.toDisplayString(resData.problem),
                      5
                      /* TEXT, STYLE */
                    )
                  ])
                ]),
                vue.createElementVNode("view", { class: "jiesaho" }, [
                  vue.createElementVNode("view", { class: "disease-title" }, "可能症状"),
                  vue.createElementVNode("image", {
                    class: "jieshao-img",
                    src: _imports_4$1
                  }),
                  vue.createElementVNode("view", { class: "jieshao-text" }, "口腔癌是发生在口腔的恶性肿瘤之总称，大部分属于鳞状上皮细胞癌，即所谓的黏膜发生变异。在临床实践中口腔癌包括牙龈癌、舌癌、软硬腭癌、颌骨癌、口底癌、口咽癌、涎腺癌、唇癌、和上颌窦癌以及发生于颜面部皮肤黏膜的癌症等。口腔癌是头颈部较常见的恶性肿瘤之一。")
                ])
              ])
            ]),
            vue.createElementVNode("view", { class: "zhuangkuang-container" }, [
              vue.createElementVNode("view", { class: "health" }, [
                vue.createElementVNode("view", { class: "zhuangkuang" }, [
                  vue.createElementVNode("image", {
                    src: _imports_5$1,
                    mode: "scaleToFill",
                    class: "yachi-picture"
                  }),
                  vue.createTextVNode(" 口腔健康建议 ")
                ]),
                (vue.openBlock(true), vue.createElementBlock(
                  vue.Fragment,
                  null,
                  vue.renderList(resData.analyse, (item) => {
                    return vue.openBlock(), vue.createElementBlock("view", { class: "content" }, [
                      vue.createElementVNode(
                        "view",
                        { class: "fu-title" },
                        vue.toDisplayString(item.title),
                        1
                        /* TEXT */
                      ),
                      vue.createElementVNode("view", { class: "yinshi" }, [
                        (vue.openBlock(true), vue.createElementBlock(
                          vue.Fragment,
                          null,
                          vue.renderList(item.content, (sen) => {
                            return vue.openBlock(), vue.createElementBlock(
                              "view",
                              { class: "fu-content" },
                              vue.toDisplayString(sen),
                              1
                              /* TEXT */
                            );
                          }),
                          256
                          /* UNKEYED_FRAGMENT */
                        ))
                      ])
                    ]);
                  }),
                  256
                  /* UNKEYED_FRAGMENT */
                ))
              ])
            ])
          ])) : vue.createCommentVNode("v-if", true)
        ]);
      };
    }
  };
  const PagesCancerPageCancerPage = /* @__PURE__ */ _export_sfc(_sfc_main$2, [["__file", "G:/projects/uniapp/iot-front/pages/CancerPage/CancerPage.vue"]]);
  const _imports_0 = "/static/sanwei.png";
  const _imports_1 = "/static/0.png";
  const _imports_3 = "/static/1.png";
  const _imports_4 = "/static/2.png";
  const _imports_5 = "/static/3.png";
  const _imports_6 = "/static/4.png";
  const _imports_7 = "/static/confirm.png";
  const _imports_8 = "/static/success.png";
  const _imports_9 = "/static/mesh_tag_3_PHOTO_FRONTAL.png";
  const _imports_10 = "/static/overlay_tag_3_PHOTO_FRONTAL.png";
  const _imports_11 = "/static/mesh_tag_3_PHOTO_LEFT.png";
  const _imports_12 = "/static/overlay_tag_3_PHOTO_LEFT.png";
  const _imports_13 = "/static/mesh_tag_3_PHOTO_LOWER.png";
  const _imports_14 = "/static/overlay_tag_3_PHOTO_LOWER.png";
  const _imports_15 = "/static/mesh_tag_3_PHOTO_RIGHT.png";
  const _imports_16 = "/static/overlay_tag_3_PHOTO_RIGHT.png";
  const _imports_17 = "/static/mesh_tag_3_PHOTO_UPPER.png";
  const _imports_18 = "/static/overlay_tag_3_PHOTO_UPPER.png";
  const baseUrl = "http://192.168.234.36:5000/";
  const _sfc_main$1 = {
    __name: "ModelPage",
    setup(__props) {
      const photoName = vue.ref("");
      const confirmed = vue.ref(false);
      const fake = vue.ref(false);
      const photoTaken0 = vue.ref(false);
      const photoing0 = vue.ref(false);
      const photoUrl0 = vue.ref("nothing");
      function changeFake() {
        fake.value = !fake.value;
      }
      function takeAPhoto0() {
        photoTaken0.value = false;
        photoing0.value = true;
        formatAppLog("log", "at pages/ModelPage/ModelPage.vue:258", "开始请求");
        uni.request({
          url: baseUrl + "prepare_30",
          method: "GET",
          header: {
            "Content-Type": "application/json"
          },
          success: (res) => {
            photoing0.value = false;
            photoName.value = res.data.message;
            photoUrl0.value = `${baseUrl}shot_30/${photoName.value}`;
            formatAppLog("log", "at pages/ModelPage/ModelPage.vue:269", photoUrl0.value);
            photoTaken0.value = true;
          },
          fail: (err) => {
            formatAppLog("error", "at pages/ModelPage/ModelPage.vue:273", "请求失败", err);
          }
        });
      }
      const photoTaken1 = vue.ref(false);
      const photoing1 = vue.ref(false);
      const photoUrl1 = vue.ref("nothing");
      function takeAPhoto1() {
        photoTaken1.value = false;
        photoing1.value = true;
        formatAppLog("log", "at pages/ModelPage/ModelPage.vue:284", "开始请求");
        uni.request({
          url: baseUrl + "prepare_31",
          method: "GET",
          header: {
            "Content-Type": "application/json"
          },
          success: (res) => {
            photoing1.value = false;
            photoName.value = res.data.message;
            photoUrl1.value = `${baseUrl}shot_31/${photoName.value}`;
            photoTaken1.value = true;
          },
          fail: (err) => {
            formatAppLog("error", "at pages/ModelPage/ModelPage.vue:298", "请求失败", err);
          }
        });
      }
      const photoTaken2 = vue.ref(false);
      const photoing2 = vue.ref(false);
      const photoUrl2 = vue.ref("nothing");
      function takeAPhoto2() {
        photoTaken2.value = false;
        photoing2.value = true;
        formatAppLog("log", "at pages/ModelPage/ModelPage.vue:309", "开始请求");
        uni.request({
          url: baseUrl + "prepare_32",
          method: "GET",
          header: {
            "Content-Type": "application/json"
          },
          success: (res) => {
            photoing2.value = false;
            photoName.value = res.data.message;
            photoUrl2.value = `${baseUrl}shot_32/${photoName.value}`;
            photoTaken2.value = true;
          },
          fail: (err) => {
            formatAppLog("error", "at pages/ModelPage/ModelPage.vue:323", "请求失败", err);
          }
        });
      }
      const photoTaken3 = vue.ref(false);
      const photoing3 = vue.ref(false);
      const photoUrl3 = vue.ref("nothing");
      function takeAPhoto3() {
        photoTaken3.value = false;
        photoing3.value = true;
        formatAppLog("log", "at pages/ModelPage/ModelPage.vue:334", "开始请求");
        uni.request({
          url: baseUrl + "prepare_33",
          method: "GET",
          header: {
            "Content-Type": "application/json"
          },
          success: (res) => {
            photoing3.value = false;
            photoName.value = res.data.message;
            photoUrl3.value = `${baseUrl}shot_33/${photoName.value}`;
            photoTaken3.value = true;
          },
          fail: (err) => {
            formatAppLog("error", "at pages/ModelPage/ModelPage.vue:348", "请求失败", err);
          }
        });
      }
      const photoTaken4 = vue.ref(false);
      const photoing4 = vue.ref(false);
      const photoUrl4 = vue.ref("nothing");
      function takeAPhoto4() {
        photoTaken4.value = false;
        photoing4.value = true;
        formatAppLog("log", "at pages/ModelPage/ModelPage.vue:359", "开始请求");
        uni.request({
          url: baseUrl + "prepare_34",
          method: "GET",
          header: {
            "Content-Type": "application/json"
          },
          success: (res) => {
            photoing4.value = false;
            photoName.value = res.data.message;
            photoUrl4.value = `${baseUrl}shot_34/${photoName.value}`;
            photoTaken4.value = true;
          },
          fail: (err) => {
            formatAppLog("error", "at pages/ModelPage/ModelPage.vue:373", "请求失败", err);
          }
        });
      }
      function confirmPhoto() {
        formatAppLog("log", "at pages/ModelPage/ModelPage.vue:379", "开始请求");
        uni.request({
          url: baseUrl + "confirm_all",
          method: "GET",
          header: {
            "Content-Type": "application/json"
          },
          success: (res) => {
            confirmed.value = true;
          },
          fail: (err) => {
            formatAppLog("error", "at pages/ModelPage/ModelPage.vue:390", "请求失败", err);
          }
        });
      }
      return (_ctx, _cache) => {
        return vue.openBlock(), vue.createElementBlock("scroll-view", { class: "container" }, [
          vue.createElementVNode("view", {
            class: "top-section",
            style: { paddingTop: "50px" }
          }),
          vue.createElementVNode("view", { class: "title-section" }, [
            vue.createElementVNode("image", {
              class: "sanwei",
              src: _imports_0,
              onClick: _cache[0] || (_cache[0] = ($event) => changeFake())
            }),
            vue.createElementVNode("view", { class: "title" }, "口腔三维建模"),
            !fake.value ? (vue.openBlock(), vue.createElementBlock("view", {
              key: 0,
              class: "total"
            }, "通过按照指定角度拍摄口腔图片，全部拍摄完毕后点击确定按钮进行口腔三维建模：")) : vue.createCommentVNode("v-if", true)
          ]),
          !confirmed.value && !fake.value ? (vue.openBlock(), vue.createElementBlock("view", {
            key: 0,
            class: "actions"
          }, [
            vue.createElementVNode("view", { class: "action action0" }, [
              vue.createElementVNode("view", { class: "left-photo" }, [
                vue.createElementVNode("image", {
                  mode: "aspectFit",
                  class: "left-img",
                  src: _imports_1
                }),
                vue.createElementVNode("view", { class: "left-text" }, "请按以上角度拍摄口腔上颚")
              ]),
              vue.createElementVNode("view", { class: "right-photo" }, [
                vue.createElementVNode("view", { class: "kaishi-container" }, [
                  !photoTaken0.value && !photoing0.value ? (vue.openBlock(), vue.createElementBlock("view", {
                    key: 0,
                    class: "paizhao-button",
                    onClick: _cache[1] || (_cache[1] = ($event) => takeAPhoto0())
                  }, [
                    vue.createElementVNode("image", {
                      class: "camera-icon",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "开始拍照")
                  ])) : vue.createCommentVNode("v-if", true)
                ]),
                !photoTaken0.value && photoing0.value ? (vue.openBlock(), vue.createElementBlock("view", {
                  key: 0,
                  class: "loading1-container"
                }, [
                  vue.createElementVNode("div", { class: "loading1" }, [
                    vue.createElementVNode("div"),
                    vue.createElementVNode("div"),
                    vue.createElementVNode("div")
                  ]),
                  vue.createElementVNode("view", null, "正在调用拍摄模块...")
                ])) : vue.createCommentVNode("v-if", true),
                photoTaken0.value && !photoing0.value ? (vue.openBlock(), vue.createElementBlock("view", {
                  key: 1,
                  class: "photo-result"
                }, [
                  vue.createElementVNode("image", {
                    src: photoUrl0.value,
                    mode: "aspectFill",
                    class: "photo-result"
                  }, null, 8, ["src"]),
                  vue.createElementVNode("view", {
                    class: "restart-button confirm-button",
                    onClick: _cache[2] || (_cache[2] = ($event) => takeAPhoto0())
                  }, [
                    vue.createElementVNode("image", {
                      class: "yes",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "重新拍摄")
                  ])
                ])) : vue.createCommentVNode("v-if", true)
              ])
            ]),
            vue.createElementVNode("view", { class: "action action1" }, [
              vue.createElementVNode("view", { class: "left-photo" }, [
                vue.createElementVNode("image", {
                  mode: "aspectFit",
                  class: "left-img",
                  src: _imports_3
                }),
                vue.createElementVNode("view", { class: "left-text" }, "请按以上角度拍摄口腔下颚")
              ]),
              vue.createElementVNode("view", { class: "right-photo" }, [
                vue.createElementVNode("view", { class: "kaishi-container" }, [
                  !photoTaken1.value && !photoing1.value ? (vue.openBlock(), vue.createElementBlock("view", {
                    key: 0,
                    class: "paizhao-button",
                    onClick: _cache[3] || (_cache[3] = ($event) => takeAPhoto1())
                  }, [
                    vue.createElementVNode("image", {
                      class: "camera-icon",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "开始拍照")
                  ])) : vue.createCommentVNode("v-if", true)
                ]),
                !photoTaken1.value && photoing1.value ? (vue.openBlock(), vue.createElementBlock("view", {
                  key: 0,
                  class: "loading1-container"
                }, [
                  vue.createElementVNode("div", { class: "loading1" }, [
                    vue.createElementVNode("div"),
                    vue.createElementVNode("div"),
                    vue.createElementVNode("div")
                  ]),
                  vue.createElementVNode("view", null, "正在调用拍摄模块...")
                ])) : vue.createCommentVNode("v-if", true),
                photoTaken1.value && !photoing1.value ? (vue.openBlock(), vue.createElementBlock("view", {
                  key: 1,
                  class: "photo-result"
                }, [
                  vue.createElementVNode("image", {
                    src: photoUrl1.value,
                    mode: "aspectFill",
                    class: "photo-result"
                  }, null, 8, ["src"]),
                  vue.createElementVNode("view", {
                    class: "restart-button confirm-button",
                    onClick: _cache[4] || (_cache[4] = ($event) => takeAPhoto1())
                  }, [
                    vue.createElementVNode("image", {
                      class: "yes",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "重新拍摄")
                  ])
                ])) : vue.createCommentVNode("v-if", true)
              ])
            ]),
            vue.createElementVNode("view", { class: "action action2" }, [
              vue.createElementVNode("view", { class: "left-photo" }, [
                vue.createElementVNode("image", {
                  mode: "aspectFit",
                  class: "left-img",
                  src: _imports_4
                }),
                vue.createElementVNode("view", { class: "left-text" }, "请按以上角度拍摄牙齿左侧")
              ]),
              vue.createElementVNode("view", { class: "right-photo" }, [
                vue.createElementVNode("view", { class: "kaishi-container" }, [
                  !photoTaken2.value && !photoing2.value ? (vue.openBlock(), vue.createElementBlock("view", {
                    key: 0,
                    class: "paizhao-button",
                    onClick: _cache[5] || (_cache[5] = ($event) => takeAPhoto2())
                  }, [
                    vue.createElementVNode("image", {
                      class: "camera-icon",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "开始拍照")
                  ])) : vue.createCommentVNode("v-if", true)
                ]),
                !photoTaken2.value && photoing2.value ? (vue.openBlock(), vue.createElementBlock("view", {
                  key: 0,
                  class: "loading1-container"
                }, [
                  vue.createElementVNode("div", { class: "loading1" }, [
                    vue.createElementVNode("div"),
                    vue.createElementVNode("div"),
                    vue.createElementVNode("div")
                  ]),
                  vue.createElementVNode("view", null, "正在调用拍摄模块...")
                ])) : vue.createCommentVNode("v-if", true),
                photoTaken2.value && !photoing2.value ? (vue.openBlock(), vue.createElementBlock("view", {
                  key: 1,
                  class: "photo-result"
                }, [
                  vue.createElementVNode("image", {
                    src: photoUrl2.value,
                    mode: "aspectFill",
                    class: "photo-result"
                  }, null, 8, ["src"]),
                  vue.createElementVNode("view", {
                    class: "restart-button confirm-button",
                    onClick: _cache[6] || (_cache[6] = ($event) => takeAPhoto2())
                  }, [
                    vue.createElementVNode("image", {
                      class: "yes",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "重新拍摄")
                  ])
                ])) : vue.createCommentVNode("v-if", true)
              ])
            ]),
            vue.createElementVNode("view", { class: "action action3" }, [
              vue.createElementVNode("view", { class: "left-photo" }, [
                vue.createElementVNode("image", {
                  mode: "aspectFit",
                  class: "left-img",
                  src: _imports_5
                }),
                vue.createElementVNode("view", { class: "left-text" }, "请按以上角度拍摄牙齿右侧")
              ]),
              vue.createElementVNode("view", { class: "right-photo" }, [
                vue.createElementVNode("view", { class: "kaishi-container" }, [
                  !photoTaken3.value && !photoing3.value ? (vue.openBlock(), vue.createElementBlock("view", {
                    key: 0,
                    class: "paizhao-button",
                    onClick: _cache[7] || (_cache[7] = ($event) => takeAPhoto3())
                  }, [
                    vue.createElementVNode("image", {
                      class: "camera-icon",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "开始拍照")
                  ])) : vue.createCommentVNode("v-if", true)
                ]),
                !photoTaken3.value && photoing3.value ? (vue.openBlock(), vue.createElementBlock("view", {
                  key: 0,
                  class: "loading1-container"
                }, [
                  vue.createElementVNode("div", { class: "loading1" }, [
                    vue.createElementVNode("div"),
                    vue.createElementVNode("div"),
                    vue.createElementVNode("div")
                  ]),
                  vue.createElementVNode("view", null, "正在调用拍摄模块...")
                ])) : vue.createCommentVNode("v-if", true),
                photoTaken3.value && !photoing3.value ? (vue.openBlock(), vue.createElementBlock("view", {
                  key: 1,
                  class: "photo-result"
                }, [
                  vue.createElementVNode("image", {
                    src: photoUrl3.value,
                    mode: "aspectFill",
                    class: "photo-result"
                  }, null, 8, ["src"]),
                  vue.createElementVNode("view", {
                    class: "restart-button confirm-button",
                    onClick: _cache[8] || (_cache[8] = ($event) => takeAPhoto3())
                  }, [
                    vue.createElementVNode("image", {
                      class: "yes",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "重新拍摄")
                  ])
                ])) : vue.createCommentVNode("v-if", true)
              ])
            ]),
            vue.createElementVNode("view", { class: "action action4" }, [
              vue.createElementVNode("view", { class: "left-photo" }, [
                vue.createElementVNode("image", {
                  mode: "aspectFit",
                  class: "left-img",
                  src: _imports_6
                }),
                vue.createElementVNode("view", { class: "left-text" }, "请按以上角度拍摄牙齿正面")
              ]),
              vue.createElementVNode("view", { class: "right-photo" }, [
                vue.createElementVNode("view", { class: "kaishi-container" }, [
                  !photoTaken4.value && !photoing4.value ? (vue.openBlock(), vue.createElementBlock("view", {
                    key: 0,
                    class: "paizhao-button",
                    onClick: _cache[9] || (_cache[9] = ($event) => takeAPhoto4())
                  }, [
                    vue.createElementVNode("image", {
                      class: "camera-icon",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "开始拍照")
                  ])) : vue.createCommentVNode("v-if", true)
                ]),
                !photoTaken4.value && photoing4.value ? (vue.openBlock(), vue.createElementBlock("view", {
                  key: 0,
                  class: "loading1-container"
                }, [
                  vue.createElementVNode("div", { class: "loading1" }, [
                    vue.createElementVNode("div"),
                    vue.createElementVNode("div"),
                    vue.createElementVNode("div")
                  ]),
                  vue.createElementVNode("view", null, "正在调用拍摄模块...")
                ])) : vue.createCommentVNode("v-if", true),
                photoTaken4.value && !photoing4.value ? (vue.openBlock(), vue.createElementBlock("view", {
                  key: 1,
                  class: "photo-result"
                }, [
                  vue.createElementVNode("image", {
                    src: photoUrl4.value,
                    mode: "aspectFill",
                    class: "photo-result"
                  }, null, 8, ["src"]),
                  vue.createElementVNode("view", {
                    class: "restart-button confirm-button",
                    onClick: _cache[10] || (_cache[10] = ($event) => takeAPhoto4())
                  }, [
                    vue.createElementVNode("image", {
                      class: "yes",
                      src: _imports_2$1
                    }),
                    vue.createElementVNode("view", null, "重新拍摄")
                  ])
                ])) : vue.createCommentVNode("v-if", true)
              ])
            ]),
            vue.createElementVNode("view", { class: "paizhao-secion confirm-section" }, [
              vue.createElementVNode("view", {
                class: "paizhao-button confirm",
                onClick: _cache[11] || (_cache[11] = ($event) => confirmPhoto())
              }, [
                vue.createElementVNode("image", {
                  class: "camera-icon",
                  src: _imports_7
                }),
                vue.createElementVNode("view", null, "确认图片")
              ])
            ])
          ])) : vue.createCommentVNode("v-if", true),
          confirmed.value && !fake.value ? (vue.openBlock(), vue.createElementBlock("view", {
            key: 1,
            class: "confirm-message"
          }, [
            vue.createElementVNode("image", {
              class: "success",
              src: _imports_8
            }),
            vue.createElementVNode("view", { class: "success-message" }, "已成功将您的口腔资料发送到服务器，分析完成的结果稍后将会发送至您的邮箱")
          ])) : vue.createCommentVNode("v-if", true),
          fake.value ? (vue.openBlock(), vue.createElementBlock("view", {
            key: 2,
            class: "model-result"
          }, [
            vue.createElementVNode("view", { class: "model-text" }, "模型分析结果如下:"),
            vue.createElementVNode("view", { class: "model-text" }, "口腔正面"),
            vue.createElementVNode("view", { class: "image-item" }, [
              vue.createElementVNode("image", {
                class: "model-image image-left",
                mode: "aspectFit",
                src: _imports_9
              }),
              vue.createElementVNode("image", {
                class: "model-image image-right",
                mode: "aspectFit",
                src: _imports_10
              })
            ]),
            vue.createElementVNode("view", { class: "model-text" }, "口腔左侧"),
            vue.createElementVNode("view", { class: "image-item" }, [
              vue.createElementVNode("image", {
                class: "model-image image-left",
                mode: "aspectFit",
                src: _imports_11
              }),
              vue.createElementVNode("image", {
                class: "model-image image-right",
                mode: "aspectFit",
                src: _imports_12
              })
            ]),
            vue.createElementVNode("view", { class: "model-text" }, "口腔下部"),
            vue.createElementVNode("view", { class: "image-item" }, [
              vue.createElementVNode("image", {
                class: "model-image image-left",
                mode: "aspectFit",
                src: _imports_13
              }),
              vue.createElementVNode("image", {
                class: "model-image image-right",
                mode: "aspectFit",
                src: _imports_14
              })
            ]),
            vue.createElementVNode("view", { class: "model-text" }, "口腔右侧"),
            vue.createElementVNode("view", { class: "image-item" }, [
              vue.createElementVNode("image", {
                class: "model-image image-left",
                mode: "aspectFit",
                src: _imports_15
              }),
              vue.createElementVNode("image", {
                class: "model-image image-right",
                mode: "aspectFit",
                src: _imports_16
              })
            ]),
            vue.createElementVNode("view", { class: "model-text" }, "口腔上部"),
            vue.createElementVNode("view", { class: "image-item" }, [
              vue.createElementVNode("image", {
                class: "model-image image-left",
                mode: "aspectFit",
                src: _imports_17
              }),
              vue.createElementVNode("image", {
                class: "model-image image-right",
                mode: "aspectFit",
                src: _imports_18
              })
            ])
          ])) : vue.createCommentVNode("v-if", true)
        ]);
      };
    }
  };
  const PagesModelPageModelPage = /* @__PURE__ */ _export_sfc(_sfc_main$1, [["__file", "G:/projects/uniapp/iot-front/pages/ModelPage/ModelPage.vue"]]);
  __definePage("pages/index/index", PagesIndexIndex);
  __definePage("pages/TonguePage/TonguePage", PagesTonguePageTonguePage);
  __definePage("pages/CancerPage/CancerPage", PagesCancerPageCancerPage);
  __definePage("pages/ModelPage/ModelPage", PagesModelPageModelPage);
  const _sfc_main = {
    onLaunch: function() {
      formatAppLog("log", "at App.vue:4", "App Launch");
    },
    onShow: function() {
      formatAppLog("log", "at App.vue:7", "App Show");
    },
    onHide: function() {
      formatAppLog("log", "at App.vue:10", "App Hide");
    }
  };
  const App = /* @__PURE__ */ _export_sfc(_sfc_main, [["__file", "G:/projects/uniapp/iot-front/App.vue"]]);
  function createApp() {
    const app = vue.createVueApp(App);
    return {
      app
    };
  }
  const { app: __app__, Vuex: __Vuex__, Pinia: __Pinia__ } = createApp();
  uni.Vuex = __Vuex__;
  uni.Pinia = __Pinia__;
  __app__.provide("__globalStyles", __uniConfig.styles);
  __app__._component.mpType = "app";
  __app__._component.render = () => {
  };
  __app__.mount("#app");
})(Vue);
