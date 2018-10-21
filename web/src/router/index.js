import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const login = r => require.ensure([], () => r(require('../pages/login/login')), 'login')
const forgetPassword = r => require.ensure([], () => r(require('../pages/login/children/forgetPassword')), 'forgetPassword')

const message = r => require.ensure([], () => r(require('../pages/message/message')), 'message')
const messageDetail = r => require.ensure([], () => r(require('../pages/message/messageDetail')), 'messageDetail')

const mall = r => require.ensure([], () => r(require('../pages/mall/mall')), 'mall')
const payOrder = r => require.ensure([], () => r(require('../pages/mall/payOrder')), 'payOrder')
const mallOrder = r => require.ensure([], () => r(require('../pages/mall/order')), 'mallOrder')

const personal = r => require.ensure([], () => r(require('../pages/personal/personal')), 'personal')
const setting = r => require.ensure([], () => r(require('../pages/personal/setting')), 'setting')
const changeHeadImg = r => require.ensure([], () => r(require('../pages/personal/changeHeadImg')), 'changeHeadImg')
const changePassword = r => require.ensure([], () => r(require('../pages/personal/changePassword')), 'changePassword')
const addressList = r => require.ensure([], () => r(require('../pages/personal/addressList')), 'addressList')
const addressEdit = r => require.ensure([], () => r(require('../pages/personal/addressEdit')), 'addressEdit')

const wallet = r => require.ensure([], () => r(require('../pages/wallet/wallet')), 'wallet')
const balanceCharge = r => require.ensure([], () => r(require('../pages/wallet/balanceCharge')), 'balanceCharge')
const withdrawCash = r => require.ensure([], () => r(require('../pages/wallet/withdrawCash')), 'withdrawCash')
const balanceRecord = r => require.ensure([], () => r(require('../pages/wallet/balanceRecord')), 'balanceRecord')
const balanceRecordDetail = r => require.ensure([], () => r(require('../pages/wallet/balanceRecordDetail')), 'balanceRecordDetail')
const withdrawCashRecord = r => require.ensure([], () => r(require('../pages/wallet/withdrawCashRecord')), 'withdrawCashRecord')
const withdrawCashRecordDetail = r => require.ensure([], () => r(require('../pages/wallet/withdrawCashRecordDetail')), 'withdrawCashRecordDetail')
const marginMoney = r => require.ensure([], () => r(require('../pages/wallet/marginMoney')), 'marginMoney')

const sale = r => require.ensure([], () => r(require('../pages/sale/sale')), 'sale')


const channel = r => require.ensure([], () => r(require('../pages/channel/channel')), 'channel')

const purchase = r => require.ensure([], () => r(require('../pages/purchase/purchase')), 'purchase')

const authorization = r => require.ensure([], () => r(require('../pages/authorization/authorization')), 'authorization')

const promotion = r => require.ensure([], () => r(require('../pages/promotion/promotion')), 'promotion')
const wantInvite = r => require.ensure([], () => r(require('../pages/promotion/wantInvite')), 'wantInvite')
const newInvite = r => require.ensure([], () => r(require('../pages/promotion/newInvite')), 'newInvite')
const inviteLink = r => require.ensure([], () => r(require('../pages/promotion/inviteLink')), 'inviteLink')
const applyAgent = r => require.ensure([], () => r(require('../pages/promotion/applyAgent')), 'applyAgent')

const integratedService = r => require.ensure([], () => r(require('../pages/integratedService/integratedService')), 'integratedService')
const feedback = r => require.ensure([], () => r(require('../pages/integratedService/feedback')), 'feedback')
const linkWechat = r => require.ensure([], () => r(require('../pages/integratedService/linkWechat')), 'linkWechat')
const protocol = r => require.ensure([], () => r(require('../pages/integratedService/protocol')), 'protocol')


export const constantRouterMap = [
    {
        path: '/',
        redirect: '/login'
    }, {
        path: '/login',
        component: login,
        meta: {
            title: '登录',
        },
        children: [{
            path: 'forgetPassword',
            component: forgetPassword,
            meta: {
                title: '忘记密码',
            },
        },]
    }, {
        path: '/message',
        component: message,
        meta: {
            title: '消息',
        },
    }, {
        path: '/messageDetail',
        component: messageDetail,
        meta: {
            transitionName: 'router-slid',
            title: '公司消息详情',

        },
    },  {
        path: '/mallOrder',
        component: mallOrder,
        meta: {
            transitionName: 'router-slid',
            title: '云仓订单',

        },
    }, {
        path: '/mall',
        component: mall,
        meta: {
            title: '云仓',
        },
    }, {
        path: '/payOrder',
        component: payOrder,
        meta: {
            transitionName: 'router-slid',
            title: '结算',

        },
    },

    {
        path: '/personal',
        component: personal,
        meta: {
            title: '蓓莉云仓',
        },
    },{
        path: '/setting',
        component: setting,
        meta: {
            title: '我的信息',
        },
    },{
        path: '/changePassword',
        component: changePassword,
        meta: {
            title: '修改密码',
        },
    },{
        path: '/changeHeadImg',
        component: changeHeadImg,
        meta: {
            title: '更换头像',
        },
    },{
        path: '/addressList',
        component: addressList,
        meta: {
            title: '我的地址',
        },
    },{
        path: '/addressEdit',
        component: addressEdit,
        meta: {
            title: '地址编辑',
        },
    },

    {
        path: '/wallet',
        component: wallet,
        meta: {
            transitionName: 'router-slid',
            title: '我的钱包'
        },
    }, {
        path: '/withdrawCash',
        component: withdrawCash,
        meta: {
            transitionName: 'router-slid',
            title: '余额提现'
        },
    }, {
        path: '/balanceCharge',
        component: balanceCharge,
        meta: {
            transitionName: 'router-slid',
            title: '余额充值'
        },
    },{
        path: '/balanceRecord',
        component: balanceRecord,
        meta: {
            transitionName: 'router-slid',
            title: '收支记录'
        },
    },{
        path: '/balanceRecordDetail',
        component: balanceRecordDetail,
        meta: {
            transitionName: 'router-slid',
            title: '收支详情'
        },
    },{
        path: '/withdrawCashRecord',
        component: withdrawCashRecord,
        meta: {
            transitionName: 'router-slid',
            title: '提现记录'
        },
    },{
        path: '/withdrawCashRecordDetail',
        component: withdrawCashRecordDetail,
        meta: {
            transitionName: 'router-slid',
            title: '提现详情'
        },
    },{
        path: '/marginMoney',
        component: marginMoney,
        meta: {
            transitionName: 'router-slid',
            title: '保证金'
        },
    },


    {
        path: '/sale',
        component: sale,
        meta: {
            transitionName: 'router-slid',
            title: '我的销售',

        },
    },

    {
        path: '/channel',
        component: channel,
        meta: {
            transitionName: 'router-slid',
            title: '我的渠道',

        },
    },

    {
        path: '/purchase',
        component: purchase,
        meta: {
            title: '我的销售',

        },
    },{
        path: '/wantInvite',
        component: wantInvite,
        meta: {
            title: '我要邀请',
        },
    },{
        path: '/newInvite',
        component: newInvite,
        meta: {
            title: '新增邀请链接',

        },
    },{
        path: '/inviteLink',
        component: inviteLink,
        meta: {
            title: '邀请链接',
        },
    },{
        path: '/applyAgent',
        component: applyAgent,
        meta: {
            title: '申请代理',
        },
    },

    {
        path: '/authorization',
        component: authorization,
        meta: {
            transitionName: 'router-slid',
            title: '我的授权',
        },
    },

    {
        path: '/promotion',
        component: promotion,
        meta: {
            title: '我要推广',

        },
    },



    {
        path: '/integratedService',
        component: integratedService,
        meta: {
            transitionName: 'router-slid',
            title: '综合业务',

        },
    },{
        path: '/feedback',
        component: feedback,
        meta: {
            transitionName: 'router-slid',
            title: '问题反馈',

        },
    },{
        path: '/linkWechat',
        component: linkWechat,
        meta: {
            transitionName: 'router-slid',
            title: '微信绑定',

        },
    },{
        path: '/protocol',
        component: protocol,
        meta: {
            transitionName: 'router-slid',
            title: '代理协议',

        },
    },


];


let router = new Router({
    // mode: 'history', // require service support
    scrollBehavior: () => ({y: 0}),
    routes: constantRouterMap
})


router.beforeEach((to, from, next) => {
    /* 路由发生变化修改页面title */
    document.title = to.meta.title || '蓓莉云仓';
    next();
});

export default router;
