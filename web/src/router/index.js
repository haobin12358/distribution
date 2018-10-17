import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const login = r => require.ensure([], () => r(require('../pages/login/login')), 'login')
const forgetPassword = r => require.ensure([], () => r(require('../pages/login/children/forgetPassword')), 'forgetPassword')

const message = r => require.ensure([], () => r(require('../pages/message/message')), 'message')
const messageDetail = r => require.ensure([], () => r(require('../pages/message/children/messageDetail')), 'messageDetail')

const mall = r => require.ensure([], () => r(require('../pages/mall/mall')), 'mall')
const payOrder = r => require.ensure([], () => r(require('../pages/mall/children/payOrder')), 'payOrder')

const personal = r => require.ensure([], () => r(require('../pages/personal/personal')), 'personal')


export const constantRouterMap = [
    {
        path: '/',
        redirect: '/message'
    }, {
        path: '/login',
        component: login,
        children: [{
            path: 'forgetPassword', //食品详情页
            component: forgetPassword,
        },]
    }, {
        path: '/mall',
        component: mall,
        children: [{
            path: 'payOrder', //食品详情页
            component: payOrder,
        }],
    }, {
        path: '/message',
        component: message,
        children: [{
            path: 'messageDetail', //食品详情页
            component: messageDetail,
        }],
    }, {
        path: '/personal',
        component: personal
    },
];

export default new Router({
    // mode: 'history', // require service support
    scrollBehavior: () => ({y: 0}),
    routes: constantRouterMap
})
