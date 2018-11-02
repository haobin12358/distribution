const mock = false;
const title =mock? 'https://dsn.apizza.net/mock/d9069d5919d18f681c57c817227226df/': 'http://www.qupifar.com/api/v1/';

const api={
  login: title + 'admin/admin_login',  // 管理员登录
  modifyPassword: title + 'admin/modify_password',  // 管理员登录
  historyScore: title + 'history/history',  // 查看历史统计
  lotteryChangeList: title + 'lottery/lottery_change_list', // 查看所有的兑换列表
  agreeLotterChange: title + 'lottery/agree_lotter_change', // 查看所有的兑换列表

  updateLotteryFee: title + 'lottery/update_lottery_fee', // 奖券费率设置
  getLotteryFee: title + 'lottery/get_lottery_fee', // 奖券费率设置

  getUsersByNickname: title + 'user/get_users_by_nickname', // 模糊搜索用户名
  updateScoreStraignt: title + 'score/update_score_straignt', // 直接给用户加积分

  getServerPricescore: title + 'server/get_server_pricescore', // 获取服务价格
  updateServerPrices: title + 'server/update_server_prices', // 更新服务价格

  getLink: title + 'link/get_link', // 获取链接
  setLink: title + 'link/set_link', // 设置链接

  incomeCard: title + 'admin/income_card', // 获取收款(get)   获取收款(post)
  getBankList: title + 'cardinfo/get_bank_list', // 获取收款(get)   获取收款(post)
};

export default api
