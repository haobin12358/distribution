// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import promise from 'es6-promise';//解决axios在ie9下不生效的方法
promise.polyfill();

//ui选择elementui
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css'
import './common/css/index.less'

Vue.use(ElementUI);

import seeImage from './components/common/SeeImage';

Vue.use(seeImage);

//过滤器
import filter from './filter'

filter(Vue);

//图表
import echarts from 'echarts';

Vue.prototype.$echarts = echarts;

import axios from 'axios';

Vue.prototype.$http = axios;

import VueLazyload from 'vue-lazyload'

Vue.use(VueLazyload, {loading:"/static/images/spinner.svg" })

import api from './api/api';

Vue.prototype.$api = api;

import common from './common/js/common';

Vue.prototype.$common = common;


//拦截器、
import {Loading, Message, MessageBox} from 'element-ui'
// 超时时间
axios.defaults.timeout = 60000
// http请求拦截器
let loadinginstace;
axios.interceptors.request.use(config => {
    if (!config.noLoading) {
        loadinginstace = Loading.service({fullscreen: true});
    }
    return config
}, error => {
    Message({
        message: '加载超时',
        type: 'warning'
    });

    return Promise.reject(error);
})
// http响应拦截器
axios.interceptors.response.use(data => {// 响应成功关闭loading
    if (loadinginstace) {
        loadinginstace.close();
    }
    if (data.data.status != 200) {
        Vue.prototype.$message.error(data.data.message);
    }
    if (data.data.status == 405 && data.data.status_code == 405003) {
        location.href = location.origin;
        localStorage.setItem('token', '');
        this.$notify()
    }

    return data;
}, error => {
    Message({
        message: '请求失败',
        type: 'warning'
    });
    if (loadinginstace) {
        loadinginstace.close();
    }
    return Promise.reject(error);
})


Vue.config.productionTip = false
import store from './vuex'
/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    store,
    components: {App},
    template: '<App/>'
});
