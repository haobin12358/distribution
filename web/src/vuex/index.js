import Vue from 'vue';
import Vuex from 'vuex';
import actions from "./actions"
import mutations from "./mutations"
import getters from "./getters"

Vue.use(Vuex);

const state = {
    login: false, // 是否登录
    userInfo: {}, // 用户信息
    showAgent: true,
    notReadComMsg: 0, // 未读消息数
    cartList: [],   // 购物车数据
    chooseAddress: null,    // 下单时额外选的地址

    agentMessages: [],  // 代理消息
    companyMessages: [],    // 公司消息
    readingMessage: {}, // 正在阅读的公司消息
    updPwdCodeDisableTime: 0,
}

export default new Vuex.Store({
    state,
    getters,
    mutations,
    actions,
})
