import wx from 'weixin-js-sdk';
import axios from 'axios';
import api from '../../api/api';
const wxApi = {
  /**
   * [isweixin 判断是否微信浏览器]
   */
  isweixin () {
    const ua = window.navigator.userAgent.toLowerCase()
    if (ua.match(/MicroMessenger/i) == 'micromessenger') {
      return true
    } else {
      this.$router.push({path: '/wxkj/isnotWechat'})
      return false
    }
  },
  isWxAuth () {
    let localUid = localStorage.getItem('localUid')
    let localToken = localStorage.getItem('localToken')
    if (!localToken) {
      let token = this.$route.query.token
      let uid = this.$route.query.uid
      if (token) {
        localStorage.setItem('localToken', token)
        localStorage.setItem('localUid', uid)
      } else {
        // 将url编码后传给后端，解决微信过滤Vue hash模式 #被过滤的问题
        var u = encodeURIComponent(window.location.href)
        window.location.href = hostName + '/wxpl/oauth?forwardUrl=' + u
      }
    }
  },
  wxRegister (callback) {
    // let data = {params: {reqUrl: window.location.href}}

    axios.get(api.get_config,{
      params:{
        url:window.location.href
      }
    } ).then((res) => {
      if(res.data.status == 200)
        wx.config({
          debug: false,
          appId: res.data.data.appid,
          timestamp: res.data.data.timestamp,
          nonceStr: res.data.data.nonceStr,
          signature: res.data.data.signature,
          jsApiList: ['onMenuShareTimeline', 'onMenuShareAppMessage']
        });
    }).catch((error) => {
      console.log(error ,'1111')
    })
    wx.ready((res) => {
      // 如果需要定制ready回调方法
      wx.onMenuShareTimeline({
        title: '1111', // 分享标题
        link: 'http://www.jzdlink.com',      // 分享链接
        imgUrl: 'http://www.jzdlink.com/wordpress/wp-content/themes/wordpress_thems/images/lib/logo.png',// 分享图标
        success () {
          // 用户成功分享后执行的回调函数

        },
        cancel () {
          // 用户取消分享后执行的回调函数


        },error(){
          console.log('1112')
        }
      });
      wx.onMenuShareAppMessage({
        title: '1111', // 分享标题
        link: 'http://www.jzdlink.com',      // 分享链接
        imgUrl: 'http://www.jzdlink.com/wordpress/wp-content/themes/wordpress_thems/images/lib/logo.png',// 分享图标
        success () {
          // 用户成功分享后执行的回调函数

        },
        cancel () {
          // 用户取消分享后执行的回调函数


        },error(){
          console.log('1112')
        }
      })

    })
  },
  ShareTimeline (opstion) {
    wx.onMenuShareTimeline({
      title: opstion.title || '1111', // 分享标题
      link: opstion.link || '', // 分享链接
      imgUrl: opstion.imgUrl || '', // 分享图标
      success () {
        // 用户成功分享后执行的回调函数
        opstion.success()
      },
      cancel () {
        // 用户取消分享后执行的回调函数

        opstion.error()
      },error(){
        console.log('1112')
      }
    })
  },
  ShareAppMessage (opstion) {
    wx.onMenuShareAppMessage({
      title: opstion.title || '1111', // 分享标题
      link: opstion.link || '', // 分享链接
      imgUrl: opstion.imgUrl || '', // 分享图标
      success () {
        // 用户成功分享后执行的回调函数
        opstion.success()
      },
      cancel () {
        // 用户取消分享后执行的回调函数

        opstion.error()
      },error(){
        console.log('1112')
      }
    })
  },
  // 预览图片
  previewImage(current, urls) {
    // console.log(current, urls);
    wx.previewImage({
      current: current, // 当前显示图片的http链接
      urls: [urls], // 需要预览的图片http链接列表
      success() {
        console.log("success", current, urls);
      },
      failed() {
        console.log("failed", current, urls);
      },
      complete() {
        console.log("complete", current, urls);
      }
    });
  }

}
export default wxApi
