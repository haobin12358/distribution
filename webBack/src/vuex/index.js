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
            children: [
                {
                    title: '所有商品',
                    path: 'index',
                },{
                    title: '商品分类',
                    path: 'category',
                },
            ]
        },{
            title: '订单',
            path: '/order',
            iconPath: '/static/images/menu_profile.png',
        },{
            title: '销售',
            path: '/sale',
            iconPath: '/static/images/menu_profile.png',
            children: [
                {
                    title: '销售统计',
                    path: 'index',
                },{
                    title: '个人销售',
                    path: 'personSale',
                },
            ]
        },{
            title: '消息',
            path: '/message',
            iconPath: '/static/images/menu_profile.png',
        },{
            title: '客服',
            path: '/service',
            iconPath: '/static/images/menu_profile.png',
            children: [
                {
                    title: '用户反馈',
                    path: 'index',
                },{
                    title: '用户注册',
                    path: 'register',
                },{
                    title: '充值',
                    path: 'charge',
                },{
                    title: '提现',
                    path: 'withdraw',
                },
            ]
        },
    ],     //  主页左侧菜单
}

export default new Vuex.Store({
    state,
    getters,
    mutations,
    actions,
})
