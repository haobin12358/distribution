import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '../views/layout/Layout'

/** note: submenu only apppear when children.length>=1
 *   detail see  https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 **/

/**
 * hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
 *                                if not set alwaysShow, only more than one route under the children
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noredirect           if `redirect:noredirect` will no redirct in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']     will control the page roles (you can set multiple roles)
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
    noCache: true                if true ,the page will no be cached(default is false)
  }
 **/

const login = r => require.ensure([], () => r(require('../views/login/index')), 'login');
const forgetPwd = r => require.ensure([], () => r(require('../views/login/forgetPwd')), 'forgetPwd');


const commonLayout = r => require.ensure([], () => r(require('../views/common/commonLayout')), 'commonLayout');


const profile = r => require.ensure([], () => r(require('../views/profile/index')), 'profile');

const mall = r => require.ensure([], () => r(require('../views/mall/index')), 'mall');

const category = r => require.ensure([], () => r(require('../views/product/category')), 'category');
const product = r => require.ensure([], () => r(require('../views/product/index')), 'product');
const productEdit = r => require.ensure([], () => r(require('../views/product/productEdit')), 'productEdit');

const order = r => require.ensure([], () => r(require('../views/order/index')), 'order');
const orderDetail = r => require.ensure([], () => r(require('../views/order/detail')), 'orderDetail');

const sale = r => require.ensure([], () => r(require('../views/sale/index')), 'sale');  //  销售统计
const personSale = r => require.ensure([], () => r(require('../views/sale/person')), 'personSale'); //  个人返现

const message = r => require.ensure([], () => r(require('../views/message/index')), 'message');

const service = r => require.ensure([], () => r(require('../views/service/index')), 'service');     //反馈
const charge = r => require.ensure([], () => r(require('../views/service/charge')), 'charge');     //充值
const withdraw = r => require.ensure([], () => r(require('../views/service/withdraw')), 'withdraw');     //充值
const marginMoney = r => require.ensure([], () => r(require('../views/service/marginMoney')), 'marginMoney');     //保证金
const register = r => require.ensure([], () => r(require('../views/service/register')), 'register');     //保证金


export const constantRouterMap = [
    {
        path: '/',
        redirect: '/login',
        meta: {}
    }, {
        path: '/login',
        component: login,
        meta: {}
    }, {
        path: '/forgetPwd',
        component: forgetPwd,
        meta: {}
    },

    {
        path: '/profile',
        redirect: 'profile/index',
        component: commonLayout,
        meta: {
            requireAuth: true
        },
        children: [
            {
                path: 'index',
                component: profile,
                meta: {}
            },
        ]
    },

    {
        path: '/mall',
        redirect: 'mall/index',
        component: commonLayout,
        meta: {
            requireAuth: true

        },
        children: [
            {
                path: 'index',
                component: mall,
                meta: {}
            },
        ]
    },

    {
        path: '/product',
        redirect: 'product/index',
        component: commonLayout,
        meta: {
            requireAuth: true

        },
        children: [
            {
                path: 'index',
                component: product,
                meta: {}
            }, {
                path: 'productEdit',
                component: productEdit,
                meta: {}
            },
            {
                path: 'category',
                component: category,
                meta: {}
            },
        ]
    },

    {
        path: '/order',
        redirect: 'order/index',
        component: commonLayout,
        meta: {
            requireAuth: true

        },
        children: [
            {
                path: 'index',
                component: order,
                meta: {}
            }, {
                path: 'orderDetail',
                component: orderDetail,
                meta: {}
            },

        ]
    },

    {
        path: '/sale',
        redirect: 'sale/index',
        component: commonLayout,
        meta: {
            requireAuth: true

        },
        children: [
            {
                path: 'index',
                component: sale,
                meta: {}
            }, {
                path: 'personSale',
                component: personSale,
                meta: {}
            },
        ]
    },

    {
        path: '/message',
        redirect: 'message/index',
        component: commonLayout,
        meta: {
            requireAuth: true

        },
        children: [
            {
                path: 'index',
                component: message,
                meta: {}
            },
        ]
    },

    {
        path: '/service',
        redirect: 'service/index',
        component: commonLayout,
        meta: {
            requireAuth: true
        },
        children: [
            {
                path: 'index',
                component: service,
                meta: {}
            },  {
                path: 'withdraw',
                component: withdraw,
                meta: {}
            },  {
                path: 'charge',
                component: charge,
                meta: {}
            }, {
                path: 'register',
                component: register,
                meta: {

                }
            },
        ]
    },



]

const router = new Router({
    scrollBehavior: () => ({y: 0}),
    routes: constantRouterMap
})
router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requireAuth)) {
        if (localStorage.getItem('token')) {  // 判断当前的token是否存在
            next();
        } else {
            next({
                path: '/login',
                query: {redirect: to.fullPath}  // 将跳转的路由path作为参数，登录成功后跳转到该路由
            })
        }
    } else {
        next();
    }
});

export default router;

