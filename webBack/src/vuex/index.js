import Vue from 'vue';
import Vuex from 'vuex';
import actions from "./actions"
import mutations from "./mutations"
import getters from "./getters"

Vue.use(Vuex);

const state = {
    menu: [
        {
            title: '概览',
            path: '/profile',
            iconPath: '/static/images/menu_profile.png',
        },{
            title: '商城',
            path: '/mall',
            iconPath: '/static/images/menu_profile.png',
        },{
            title: '商品',
            path: '/product',
            iconPath: '/static/images/menu_profile.png',
        },{
            title: '订单',
            path: '/order',
            iconPath: '/static/images/menu_profile.png',
        },{
            title: '销售',
            path: '/sale',
            iconPath: '/static/images/menu_profile.png',
        },{
            title: '消息',
            path: '/message',
            iconPath: '/static/images/menu_profile.png',
        },{
            title: '客服',
            path: '/service',
            iconPath: '/static/images/menu_profile.png',
        },
    ],     //  主页左侧菜单
}

export default new Vuex.Store({
    state,
    getters,
    mutations,
    actions,
})
