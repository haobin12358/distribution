const mock = false;
const title =mock? 'https://dsn.apizza.net/mock/d9069d5919d18f681c57c817227226df/': 'https://beiliserver.daaiti.cn:443';

const api={
    login: title+'/admin/login',                              //  登录
    updatePwd: title+'/admin/update_pwd',                     //  修改密码

    uploadFile: title+'/user/upload_file?token='+ localStorage.getItem('token'),                     //  修改密码


    getComMessage: title+'/message/get_com_message',          //  公司消息列表
    publishComMessage: title+'/message/publish_commessage',   //  发布公司消息
    deleteComMessage: title+'/message/delete_commessage',     //  删除消息


    getProductCategoryList: title+'/product/get_product_category_list',   //  商品分类
    addProductCategory: title+'/product/add_product_category',
    updateCategory: title+'/product/update_category',
    deleteCategory: title+'/product/delete_category',

    getProductList: title+'/product/get_product_list',          //  商品

    getAllOrder: title+'/order/get_all_order',                  //  订单
    updateOrder: title+'/order/update_order',

    getAllUserAcount: title+'/account/get_alluser_account',     //  个人销售
    getDirectagentPerformance: title+'/account/get_directagent_performance',    //  直属销售量



};

export default api
