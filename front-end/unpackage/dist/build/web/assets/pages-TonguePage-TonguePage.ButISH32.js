import{r as A,a,c as s,w as e,S as l,o as t,b as o,d as c,e as g,f as n,t as u,g as i,h as r,F as C,i as d,j as f,k as Q,n as I}from"./index-Czds8fzW.js";import{_ as B}from"./shetou.qP5zUlIe.js";import{_ as p,a as h}from"./_plugin-vue_export-helper.Cio2fkwX.js";import{_ as w,b as E,a as v}from"./oral.Jn1c4I4w.js";const y=""+new URL("digest-Dvv_EWOM.png",import.meta.url).href,F="http://192.168.234.36:5000/",m=p({__name:"TonguePage",setup(p){const m=["#c2e9fb","#f5efef","#d8fee1"],K=["#4481eb","#ed6ea0","#6fe186"],b=A(!1),k=A(!1),H=A(!1),S=A("nothing"),x=A(""),R=a({condition:[],analyse:[]}),U=A(!1),O=A(!1),G=A("");function V(){O.value=!0,console.log("开始请求"),d({url:F+"prepare_tongue",method:"GET",header:{"Content-Type":"application/json"},success:A=>{O.value=!1,x.value=A.data.message,S.value=`${F}shot_tongue/${x.value}`,k.value=!0},fail:A=>{console.error("请求失败",A)}})}return(A,a)=>{const p=f,j=Q,q=l;return t(),s(q,{class:"container","scroll-y":"true"},{default:e((()=>[b.value?g("",!0):(t(),s(p,{key:0,class:"photo-section"},{default:e((()=>[o(p,{class:"top-section",style:{paddingTop:"50px"}}),o(p,{class:"take-photo"},{default:e((()=>[k.value||O.value?g("",!0):(t(),s(p,{key:0,class:"photo-icon"},{default:e((()=>[o(j,{class:"kouqiang-icon",src:B}),o(p,{class:"paizhao-secion"},{default:e((()=>[o(p,{class:"paizhao-button",onClick:a[0]||(a[0]=A=>V())},{default:e((()=>[o(j,{class:"camera-icon",src:h}),o(p,null,{default:e((()=>[c("开始拍照")])),_:1})])),_:1}),o(p,{class:"phone-text"},{default:e((()=>[c("请将摄像头按照对准舌苔，确保拍摄角度与上图一致。")])),_:1})])),_:1})])),_:1})),O.value?(t(),s(p,{key:1,class:"loading1-container"},{default:e((()=>[n("div",{class:"loading1"},[n("div"),n("div"),n("div")]),o(p,null,{default:e((()=>[c("正在调用拍摄模块...")])),_:1})])),_:1})):g("",!0),!k.value||U.value||O.value?g("",!0):(t(),s(p,{key:2,class:"photo-result"},{default:e((()=>[o(j,{src:S.value,mode:"scaleToFill",class:"yachi"},null,8,["src"]),o(p,{class:"confirm-button-container"},{default:e((()=>[o(p,{class:"restart-button confirm-button",onClick:a[1]||(a[1]=A=>V())},{default:e((()=>[o(j,{class:"yes",src:h}),o(p,null,{default:e((()=>[c("重新拍摄")])),_:1})])),_:1}),o(p,{class:"confirm-button",onClick:a[2]||(a[2]=A=>(console.log("确认图片"),U.value=!0,void d({url:F+"confirm_shot_tongue/"+x.value,method:"GET",header:{"Content-Type":"application/json"},success:A=>{U.value=!1,console.log(A),R.condition=A.data.message.condition,R.analyse=A.data.message.analyse,b.value=!0},fail:A=>{console.error("请求失败",A)}})))},{default:e((()=>[o(j,{class:"yes",src:w}),o(p,null,{default:e((()=>[c("确认图片")])),_:1})])),_:1})])),_:1})])),_:1})),k.value&&U.value?(t(),s(p,{key:3,class:"loading-container"},{default:e((()=>[n("div",{class:"loading"}),o(p,null,{default:e((()=>[c("正在分析消化健康状况...")])),_:1})])),_:1})):g("",!0)])),_:1}),U.value?g("",!0):(t(),s(p,{key:0,class:"take-photo"},{default:e((()=>[H.value?g("",!0):(t(),s(p,{key:0,class:"photo-icon"},{default:e((()=>[o(p,{class:"ph-group",onClick:a[3]||(a[3]=A=>(console.log("take a ph"),void d({url:F+"phtest",method:"GET",header:{"Content-Type":"application/json"},success:A=>{console.log("ph调用成功"),console.log(A),G.value=A.data.message,H.value=!0},fail:A=>{console.error("请求失败",A)}})))},{default:e((()=>[o(j,{class:"camera-icon",src:"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAACgCAYAAACLz2ctAAAAAXNSR0IArs4c6QAABqNJREFUeF7tnWG20zYQRqOVFHbSt5KWlRRWUroS6EpgJ+qbxob3cmKPvonN55fc/AEOE419dTOyZMVpJ14QMBJoxtykhsAJAZHASgABrfhJjoA4YCWAgFb8JEdAHLASQEArfpIjIA5YCSCgFT/JERAHrAQQ0Iqf5AiIA1YCCGjFT3IExAErAQS04ic5AuKAlQACWvGTHAFxwEoAAa34SY6AOGAlgIBW/CRHQBywEkBAK36SIyAOWAkgoBU/yREQB6wEENCKn+QIiANWAghoxU9yBMQBKwEEtOInOQLigJUAAlrxkxwBccBKAAGt+EmOgDhgJYCAVvwkR0AcsBI4tIC993d70Wmtfd+j7cox73Use5zf1m0eVsDe+++n0+nL1id80d7X6d/x5z9biNB77+Ixf2itfRbfczfhjy7gZUeGiJ9aa7OYckcjoIYMAa/zCgGjMsnDNAIioEZgOTrke1IlREANPxUw5xUSDg/JCJgDfRmBgGO83o9WQgQcAzpHIeAYr+HhGAHHgCKgximiP7bWPmVvQ8CM0Ov/pwJqvNKhGAE1oAio8UqrIAJqQBFQ4xXRq1UQATWg9yZgTBbWFo/j3vKt95dXqyACPraA6Zpd7/3P0+n01w0ifm2tPS1hRkAETBeNpx0rsdGhWg0Xh2EERMBUwBlR7/1bUcLFHSwIiICKgNUtX59bax+uoUZABBwWMFAVqyACap4tRt/bLDidhFySeK5YMSH5KPJcnIhQATWSCHje9h/Xgsrre2vt/d5D8LQr/I/pOvVywhTLTZvt5FZOfsvYhxewOgw/3xe+ym6LCjiJF5U5rlFHXrGlP3ZyyxtoRxrfMwYBz9eBsSQz2tlzf1xdirlVwOIlweox7SnQrW0j4FnAv5/voMQCtfLaXMDicVwec7phQjnJvWMRsC7g1QlPtQLeWPnerIQIeBawMhO+uhhdEXCaTKgTobXilO7a2buyjbaPgMcQ8JZ700t9/SaGYgSsD8FbVcCYuVbvSb/5KoiA9VnwVteAo6OVGre4Vqk2tGc8At6vgOHN4YdhBDwLqD7PZbFzi23tVWQO/9yZhxdw2hsoz0A3vBOyJt+t14eLmyb2Ml5tFwFrSzBb3gt+2Wf/39uNZZn5ttr0AYmFcvVOTbS7untblWWP+IcWsFr9nmetW27Hmvs12+pfWas8LVXqPWSqtPnoApY69Rn04kJv8RowrVTVDwsCVj4W54lBZbfy8H7AYvvz2SzmKQo4NFutbJ5FwAMKWLz19uNM1jq1IODwel3luBHwIAJOX8f8bbqYr1zQz2ey9feCh+/bVqo2Av5aAYvZpLdt/WSEXS8bEFDq25/BlU97MZXytnS4LAzBCKj0wK+KPaiA6XC5s4Dy91eogEVjDyhgulQSp4qAWoff2zqgdvbj0enQOzeFgONQIxIBx3gp12nqxgalbYbgsf66PepAQ/CwIAzBer9TAdeZSfIhIALqBK6/I7ZBxV466TkzCKjjpwK+ZhbixRMGyj8eyCREkxABz7xCuH9vEY9ZsCbeHH2PAq49H+XlM6Tj7yGdPMyuoaYCaiLem4D270AgIAKWr980dNejEVCjSAXUeKXRCJgiehWAgBqvNBoBU0QIqCHSohFQ40UF1Hil0QiYIqICaoi0aATUeFEBNV5pNAKmiKiAGiItGgE1XlRAjVcajYApIiqghkiLRkCNFxVQ45VGI2CKiAqoIdKiEVDjRQXUeKXRCJgiogJqiLRoBNR4UQE1Xmk0AqaIqIAaIi0aATVeVECNVxqNgCkiKqCGSItGQI0XFVDjlUYjYIqICqgh0qIRUONFBdR4pdEImCKiAmqItGgE1HhRATVeaTQCpoiogBoiLRoBNV5UQI1XGo2AKSIqoIZIi0ZAjRcVUOOVRiNgiogKqCHSohFQ40UF1Hil0QiYIqICaoi0aATUeB29AsbPqSqveLrpps/7U5JHbO/9i/ieeKTc2jMNfzT34serh1O01p6Ggw2BhxXQwIKUBgIIaIBOyp8EEBAbrAQQ0Iqf5AiIA1YCCGjFT3IExAErAQS04ic5AuKAlQACWvGTHAFxwEoAAa34SY6AOGAlgIBW/CRHQBywEkBAK36SIyAOWAkgoBU/yREQB6wEENCKn+QIiANWAghoxU9yBMQBKwEEtOInOQLigJUAAlrxkxwBccBKAAGt+EmOgDhgJYCAVvwkR0AcsBJAQCt+kiMgDlgJIKAVP8kREAesBBDQip/kCIgDVgIIaMVPcgTEASsBBLTiJ/l/E5SY3SjaCboAAAAASUVORK5CYII="}),o(p,null,{default:e((()=>[c("开始检测")])),_:1})])),_:1}),o(p,{class:"ph-text"},{default:e((()=>[c("请将ph检测探头放入待检测液中，并点击ph检测按钮进行检测（可选）")])),_:1})])),_:1})),o(p,{class:"ph-container"},{default:e((()=>[H.value?(t(),s(p,{key:0,class:"ph-result"},{default:e((()=>[o(j,{class:"ph-result-img",src:"data:image/png;base64,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"}),o(p,{class:"ph-result-text"},{default:e((()=>[c("PH检测结果:"+u(G.value),1)])),_:1})])),_:1})):g("",!0)])),_:1})])),_:1}))])),_:1})),b.value?(t(),s(p,{key:1,class:"analyse-section"},{default:e((()=>[o(p,{class:"top-section",style:{paddingTop:"30px"}}),o(p,{class:"photo-text"},{default:e((()=>[c("舌苔结果分析")])),_:1}),o(p,{class:"photo"},{default:e((()=>[o(p,{class:"picture-container"},{default:e((()=>[o(j,{class:"picture",src:S.value,mode:"widthFix"},null,8,["src"])])),_:1})])),_:1}),o(p,{class:"zhuangkuang-container"},{default:e((()=>[o(p,{class:"health"},{default:e((()=>[o(p,{class:"zhuangkuang"},{default:e((()=>[o(j,{src:E,mode:"scaleToFill",class:"yachi-picture"}),c(" 舌苔健康状况 ")])),_:1}),(t(!0),i(C,null,r(R.condition,(A=>(t(),s(p,{class:"content"},{default:e((()=>[o(p,{class:"fu-title"},{default:e((()=>[c(u(A.title),1)])),_:2},1024),o(p,{class:"yinshi"},{default:e((()=>[(t(!0),i(C,null,r(A.content,(A=>(t(),s(p,{class:"fu-content"},{default:e((()=>[c(u(A),1)])),_:2},1024)))),256))])),_:2},1024)])),_:2},1024)))),256))])),_:1})])),_:1}),o(p,{class:"zhuangkuang-container"},{default:e((()=>[o(p,{class:"health"},{default:e((()=>[o(p,{class:"zhuangkuang"},{default:e((()=>[o(j,{src:y,mode:"scaleToFill",class:"yachi-picture"}),c(" ph检测分析 ")])),_:1}),o(p,{class:"content"},{default:e((()=>[o(p,{class:"yinshi"},{default:e((()=>[o(p,{class:"fu-content"},{default:e((()=>[c("口腔pH值为6.86,正常口腔PH值范围为6.6-7.0，因此您的口腔PH值在正常范围内。")])),_:1})])),_:1})])),_:1})])),_:1})])),_:1}),o(p,{class:"fangan-container"},{default:e((()=>[o(p,{class:"fangan-content"},{default:e((()=>[o(p,{class:"fangan-title"},{default:e((()=>[o(j,{src:v,mode:"scaleToFill",class:"advice-picture"}),c(" 护理建议 ")])),_:1}),(t(!0),i(C,null,r(R.analyse,(A=>(t(),s(p,{class:"fangan-list"},{default:e((()=>[(t(!0),i(C,null,r(A.content,((A,a)=>(t(),s(p,{class:"fangan-item"},{default:e((()=>[o(p,{class:"dot dot1",style:I({backgroundColor:K[a%3]})},null,8,["style"]),o(p,{class:"text-section-1",style:I({color:K[a%3],backgroundColor:m[a%3]})},{default:e((()=>[c(u(A),1)])),_:2},1032,["style"])])),_:2},1024)))),256))])),_:2},1024)))),256))])),_:1})])),_:1})])),_:1})):g("",!0)])),_:1})}}},[["__scopeId","data-v-00f39c87"]]);export{m as default};
