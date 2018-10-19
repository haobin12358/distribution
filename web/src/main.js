// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import 'lib-flexible'
Vue.config.productionTip = false

//mint-ui
import Mint from 'mint-ui';
Vue.use(Mint);
Vue.prototype.$toast = Mint.Toast;

import headerTop from "components/header/header"
Vue.component('header-top',headerTop)
import loadMore from "components/common/loadMore"
Vue.component('load-more',loadMore)
Vue.prototype.$log = console.log;

import 'mint-ui/lib/style.css'
import VueClipboard from 'vue-clipboard2'

VueClipboard.config.autoSetContainer = true // add this line
Vue.use(VueClipboard)

//处理移动端click事件300毫秒延迟。
import FastClick from 'fastclick'
FastClick.attach(document.body);

import promise from 'es6-promise';//解决axios在ie9下不生效的方法
promise.polyfill();

Vue.prototype.$http = axios;
//拦截器、
import { Indicator } from 'mint-ui';

// 超时时间
axios.defaults.timeout = 60000

//http请求拦截器
var loadinginstace
axios.interceptors.request.use(config => {
  // element ui Loading方法
  // loadinginstace = Loading.service({ fullscreen: true });
  // console.log(loadinginstace)
  Indicator.open({ text: '加载中...', spinnerType: 'fading-circle' });
  return config
}, error => {
  // Message({
  //   message:'加载超时',
  //   type:'warning'
  // });
  // loadinginstace.close()
  Indicator.close();
  return Promise.reject(error)
})
// http响应拦截器
axios.interceptors.response.use(data => {// 响应成功关闭loading
  if(data.data.status != 200 && data.data.status != 302){
    Toast({message:data.data.message});
  }

  Indicator.close();
  return data
}, error => {
  // Message({
  //   message:'请求失败',
  //   type:'warning'
  // });
  // loadinginstace.close()
  Indicator.close();
  return Promise.reject(error)
})

//引入微信
import 'weixin-js-sdk';

import store from './vuex'
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
});
