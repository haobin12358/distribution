import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const message = r => require.ensure([], () => r(require('../pages/message/message')), 'message')

const home = r => require.ensure([], () => r(require('../pages/home/index')), 'home')

const personal = r => require.ensure([], () => r(require('../pages/personal/personal')), 'personal')


export const constantRouterMap = [
  {
    path: '/',
    redirect: '/home'
  },{
    path: '/home',
    component: home
  },{
    path: '/message',
    component: message
  },{
    path: '/personal',
    component: personal
  },
];

export default new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})
