import Vue from 'vue';
import Vuex from 'vuex';
import actions from "./actions"
import mutations from "./mutations"
import getters from "./getters"

Vue.use(Vuex);

const state = {
  login: false, // 是否登录
  userInfo: {}, // 用户信息
}

export default new Vuex.Store({
  state,
  getters,
  mutations,
  actions,
})
