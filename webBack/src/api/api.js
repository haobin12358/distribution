const mock = false;
const title = mock ? 'https://dsn.apizza.net/mock/d9069d5919d18f681c57c817227226df/' : 'https://beiliserver.daaiti.cn:443';

const api = {
    login: title + '/admin/login',                              //  登录
    updatePwd: title + '/admin/update_pwd',                     //  修改密码

    uploadFile: `${title}/user/upload_file?token=${localStorage.getItem('token')}`,                     //  修改密码
    removeFile: title + '/user/remove_file',                     //  删除文件


    getComMessage: title + '/message/get_com_message',          //  公司消息列表
    publishComMessage: title + '/message/publish_commessage',   //  发布公司消息
    deleteComMessage: title + '/message/delete_commessage',     //  删除消息


    getProductCategoryList: title + '/product/get_product_category_list',   //  商品分类
    getProductCategory: title + '/product/get_product_category',   //  商品分类
    addProductCategory: title + '/product/add_product_category',
    updateCategory: title + '/product/update_category',
    deleteCategory: title + '/product/delete_category',

    getProductList: title + '/product/get_product_list',          //  商品
    saveProduct: title + '/product/create_update_product',          //  保存商品
    withdrawProduct: title + '/product/withdraw_product',          //  下架商品

    getAllOrder: title + '/order/get_all_order',                  //  订单
    updateOrder: title + '/order/update_order',

    getAllUserAcount: title + '/account/get_alluser_account',     //  个人销售
    getDirectagentPerformance: title + '/account/get_directagent_performance',    //  直推详情
    getAllPerformance: title + '/account/get_all_performance',    //  销售折扣详情

    getAlluserDrawmoneyList: title + '/account/get_alluser_drawmoney_list',    //  提现
    dealDrawmoney: title + '/account/deal_drawmoney',    //  提现

    getAllChargemoney: title + '/account/get_all_chargemoney',    //  充值
    dealChargemoney: title + '/account/deal_chargemoney',    //  充值

    getRegisterRecord: title + '/user/get_register_record',    //  注册
    dealRegisterRecord: title + '/user/deal_register_record',    //  处理注册
};

export default api
