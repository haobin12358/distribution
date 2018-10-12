import Vue from 'vue'
import Router from 'vue-router'
import Layout from '../pages/layout/index';

Vue.use(Router)


export const constantRouterMap = [
  {
    path: '/',
    component: Layout,
    redirect: 'home/index',
    children: [{
      path: 'index',
      component: () => import('../pages/home/index'),
      name: 'home',
      meta: { title: 'home', icon: 'home', noCache: true }
    }],
  },{
    path: '/home',
    component: Layout,
    redirect: 'home/index',
    children: [{
      path: 'index',
      component: () => import('../pages/home/index'),
      meta: { title: 'home', icon: 'home', noCache: true }
    }],
  },
];

export default new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})
