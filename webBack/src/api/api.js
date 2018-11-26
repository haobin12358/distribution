const mock = false;
const title = mock ? 'https://dsn.apizza.net/mock/d9069d5919d18f681c57c817227226df/' : 'https://beiliserver.daaiti.cn:443';

const api = {
    login: title + '/admin/login',                              //  登录
    updatePwd: title + '/admin/update_pwd',                     //  修改密码

    uploadFile: `${title}/user/upload_file?token=`,                     //  修改密码
    removeFile: title + '/user/remove_file',                     //  删除文件


    getComMessage: title + '/message/get_com_message',          //  公司消息列表
    publishComMessage: title + '/message/publish_commessage',   //  发布公司消息
    deleteComMessage: title + '/message/delete_commessage',     //  删除消息


    getProductCategoryList: title + '/product/get_product_category_list',   //  商品分类
    getProductCategory: title + '/product/get_product_category',   //  商品分类
    addProductCategory: title + '/product/add_product_category',
    updateCategory: title + '/product/update_category',
    deleteCategory: title + '/product/delete_category',

    getColor: title + '/product/get_color', //  颜色
    addColor: title + '/product/add_color',

    getSize: title + '/product/get_size', //  尺码
    addSize: title + '/product/add_size',

    getProductList: title + '/product/get_product_list',          //  商品
    saveProduct: title + '/product/create_update_product',          //  保存商品
    withdrawProduct: title + '/product/withdraw_product',          //  下架商品
    getProductDetails: title + '/product/get_product_details',          //  下架商品

    getAllOrder: title + '/order/get_all_order',                  //  订单
    updateOrder: title + '/order/update_order',
    getWillSendProducts: title + '/order/get_willsend_products',    //  导出

    getAllUserAcount: title + '/account/get_alluser_account',     //  个人销售
    getDirectagentPerformance: title + '/account/get_directagent_performance',    //  直推详情
    getAllPerformance: title + '/account/get_all_performance',    //  销售折扣详情
    dealRewardDiscount: title + '/account/deal_reward_discount',    //  销售折扣详情

    getAlluserDrawmoneyList: title + '/account/get_alluser_drawmoney_list',    //  提现
    dealDrawmoney: title + '/account/deal_drawmoney',    //  提现

    getAllChargemoney: title + '/account/get_all_chargemoney',    //  充值
    dealChargemoney: title + '/account/deal_chargemoney',    //  充值

    getRegisterRecord: title + '/user/get_register_record',    //  注册
    dealRegisterRecord: title + '/user/deal_register_record',    //  处理注册

    getAllUserBailRecord: title + '/account/get_alluser_bailrecord',    //  保证金
    dealBailRecord: title + '/account/deal_bailrecord',    //  处理保证金

    getSevenDaysData: title + '/account/get_sevendays_data',    //  获取近7天数据

    getCommentList: title + '/mycenter/get_comment_list',    //  评论列表
    dealComments: title + '/mycenter/deal_comments',    //  处理评论

    getSowingMap: title + '/product/get_sowingmap',    //  获取轮播图
    addSowingMap: title + '/product/add_sowingmap',    //  设置轮播图
    deleteSowingMap: title + '/product/delete_sowingmap',    //  删除轮播图

    getCountData: title + '/account/get_count_data',    //  获取统计数据
    getThisYearDate: title + '/account/get_thisyear_date',    //  获取统计数据
    getThisMonthAgentnum: title + '/account/get_thismonth_agentnum',    //  获取统计数据

    getDiscountRuler: title + '/account/get_discountruler',    //  获取
    updateDiscountRuler: title + '/account/update_discountruler',    //  获取统计数据

    updateAccounts: title + '/account/update_accounts',    //  修改密码

    getConfigure: title + '/account/get_configure',    //  获取统计数据
    updateConfigure: title + '/account/update_configure',    //  获取统计数据

};

export default api
