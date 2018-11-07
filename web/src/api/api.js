import axios from "axios"
import {Indicator, Toast} from "mint-ui"
import {getStore,setStore} from "src/common/js/mUtils"
import {TOKEN} from "src/common/js/const"

const debug = false;
export const title = debug ? 'https://dsn.apizza.net/mock/60c954072cfff536376e5acb0392c590' : 'https://beiliserver.daaiti.cn:443';

const myAxios = async (url, {params, data, method = 'get', showIndicator = true}) => {
    if (showIndicator) {
        Indicator.open({text: '加载中...', spinnerType: 'fading-circle'});
    }

    let res = await axios({
        baseURL: title,    //todo 代理
        method: method,
        url: url,
        params: params,
        data: data,
    }).catch(
        evt => {
            if (showIndicator) {
                Indicator.close();
            }

            Toast('服务器出错!');
        }
    )

    if (showIndicator) {
        Indicator.close();
    }

    if (res && res.status == 200) {
        if (res.data.status == 200) {
            this.$router.push('/login');
            setStore(TOKEN, '');
            return res.data;
        } else {
            Toast(res.data.message);
            if(res.data.status == 405 && res.data.status_code == 405003){
                this.$router.push('/login');
                setStore(TOKEN, '');
            }
            return
        }
    }
}

/**
 * 登录
 * @param username
 * @param password
 * @returns {Promise<*|undefined>}
 */
export const login = (username, password) => myAxios('/user/login', {
    method: 'post',
    data: {
        usphonenum: username,
        uspassword: password
    }
});
/**
 * 获取用户基本信息
 * @returns {Promise<*|undefined>}
 */
export const getUserBasicInfo = () => myAxios('/mycenter/get_user_basicinfo', {
    params: {
        token: getStore(TOKEN),
    }
});
/**
 * 获取用户全部信息
 * @returns {Promise<*|undefined>}
 */
export const getUserTotalInfo = () => myAxios('/mycenter/get_user_totalinfo', {
    params: {
        token: getStore(TOKEN),
    }
});
/**
 * 获取验证码
 * @param phone
 * @returns {Promise<*|undefined>}
 */
export const getInforcode = (phone) => myAxios('/mycenter/get_inforcode', {
    params: {
        usphonenum: phone,
    }
});
/**
 * 验证码校验
 * @param phone
 * @returns {Promise<*|undefined>}
 */
// export const checkInforcode = (phone, code) => myAxios('/mycenter/check_inforcode', {
//     method: 'post',
//     data: {
//         usphonenum: phone,
//         iccode: code
//     }
// });
/**
 * 修改密码
 * @param oldpassword
 * @param newpassword
 * @returns {Promise<*|undefined>}
 */
export const updatePwd = (oldpassword, newpassword) => myAxios('/user/update_pwd', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        oldpassword,
        newpassword
    }
});
/**
 * 找回密码
 * @param usphonenum
 * @param iccode
 * @param newpassword
 * @returns {Promise<*|undefined>}
 */
export const findBackPwd = (usphonenum, iccode, newpassword) => myAxios('/user/findback_pwd', {
    method: 'post',
    data: {
        usphonenum,
        iccode,
        newpassword
    }
});

/**
 * 更换头像
 * @param file  string
 * @returns {Promise<*|undefined>}
 */
export const updateHeadImg = (url) => myAxios('/mycenter/update_headimg', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        url
    }
});
/**
 * 获取收货地址
 * @param isdefault
 * @param all
 * @param UAid
 * @returns {Promise<*|undefined>}
 */
export const getUserAddress = (isdefault, all, UAid) => myAxios('/mycenter/get_useraddress', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        isdefault,
        all,
        UAid
    }
});
//  获取所有地区
export const getAllArea = () => myAxios('/mycenter/get_all_area', {
    showIndicator: false,
});
/**
 * 新增收货地址
 * @param USname
 * @param USphonenum
 * @param details
 * @param areaid
 * @returns {Promise<*|undefined>}
 */
export const addUserAddress = (USname, USphonenum, details, areaid, cityid) => myAxios('/mycenter/add_useraddress', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        USname,
        USphonenum,
        details,
        areaid,
        cityid,
    }
});
/**
 * 修改收货地址
 * @param UAid
 * @param USname
 * @param USphonenum
 * @param details
 * @param areaid
 * @returns {Promise<*|undefined>}
 */
export const updateUserAddress = (UAid, USname, USphonenum, details, areaid, cityid) => myAxios('/mycenter/update_useraddress', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        UAid,
        USname,
        USphonenum,
        details,
        areaid,
        cityid,
    }
});

export const deleteUserAddress = (UAid) => myAxios('/mycenter/delete_useraddress', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        UAid,
    }
});

export const changeDefaultAddress = (old_defaultid, new_defaultid) => myAxios('/mycenter/change_default', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        old_defaultid,
        new_defaultid,
    }
});


/**
 * 获取代理消息列表
 * @param token
 * @param page
 * @param count
 * @returns {Promise<*|undefined>}
 */
export const getAgentMessage = (page, count = 10) => myAxios('/message/get_agent_message', {
    showIndicator: false,
    params: {
        token: getStore(TOKEN),
        page,
        count,
    }
});
/**
 * 获取公司消息列表
 * @param page
 * @param count
 * @returns {Promise<*|undefined>}
 */
export const getCompanyMessage = (page, count = 10) => myAxios('/message/get_com_message', {
    showIndicator: false,
    params: {
        token: getStore(TOKEN),
        page,
        count,
    }
});
/**
 * 获取公司消息详情
 * @param messageid
 * @returns {Promise<*|undefined>}
 */
export const getCommessageDetails = (messageid) => myAxios('/message/get_commessage_details', {
    showIndicator: false,
    params: {
        token: getStore(TOKEN),
        messageid
    }
});

/**
 * 获取类别列表
 * @param PAtype    类目级别，1获取第一级类别，2获取第二级类别，项目中最高两级类别
 * @param PAid  父类别id，第一类别的父分类id为0
 * @returns {Promise<*|undefined>}
 */
export const getProductCategory = (PAtype, PAid) => myAxios('/product/get_product_category', {
    params: {
        PAtype,
        PAid
    }
});
/**
 * 获取商品列表
 * @param PAtype    类别等级,获取所有商品填非空任意值
 * @param PAid  类别id，0时获取所有商品
 * @param PRstatus  商品状态，1出售中2已售罄3已下架，0代表全部状态
 * @param page_num
 * @param page_size
 * @returns {Promise<*|undefined>}
 */
export const getProductList = (PAtype, PAid, PRstatus, page_num, page_size = 10) => myAxios('/product/get_product_list', {
    params: {
        PAtype,
        PAid,
        page_size,
        page_num,
        PRstatus
    }
});
/**
 * 获取商品详情
 * @param PRid
 * @returns {Promise<*|undefined>}
 */
export const getProduct = (PRid) => myAxios('/product/get_product', {
    params: {
        PRid
    }
});

/**
 * 创建订单
 * @param UAid  地址id
 * @param product_list  商品列表
 * @param OInote    备注
 * @param PRlogisticsfee    快递费
 * @param totalprice    总价
 * @returns {Promise<*|undefined>}
 */
export const createOrder = (UAid, product_list, OInote, PRlogisticsfee, totalprice) => myAxios('/order/create_order', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        UAid,
        product_list,
        OInote,
        PRlogisticsfee,
        totalprice,
    }
});
/**
 * 获取订单列表
 * @param type  0为全部订单，1已待发货，2为已发货，3为已完成
 * @returns {Promise<*|undefined>}
 */
export const getOrderList = (type, page, count = 10) => myAxios('/order/get_order_list', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        type,
        page,
        count,
    }
});
/**
 * 获取订单详情
 * @param OIsn  订单编号
 * @returns {Promise<*|undefined>}
 */
export const getOrderDetails = (OIsn) => myAxios('/order/get_order_details', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        OIsn
    }
});

/**
 * 获取业绩排行榜
 * @param month
 * @returns {Promise<*|undefined>}
 */
export const getRankList = (month) => myAxios('/account/get_rank_list', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        month
    }
});
/**
 * 获取金额信息(直推奖励，销售折扣，团队销量)
 * @param month
 * @returns {Promise<*|undefined>}
 */
export const getAccount = (month) => myAxios('/account/get_account', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        month
    }
});

/**
 * 获取所有直属代理
 * @returns {Promise<*|undefined>}
 */
export const getDirectagent = () => myAxios('/account/get_directagent', {
    params: {
        token: getStore(TOKEN),
    }
});
/**
 * 获取所有分销商代理
 * @returns {Promise<*|undefined>}
 */
export const getDistribute = () => myAxios('/account/get_distribute', {
    params: {
        token: getStore(TOKEN),
    },
});

/**
 * 获取二维码列表
 * @returns {Promise<*|undefined>}
 */
export const getQrcode = () => myAxios('/user/get_qrcode', {
    params: {
        token: getStore(TOKEN),
    },
});
/**
 * 添加二维码
 * @param overtime
 * @param number
 * @returns {Promise<*|undefined>}
 */
export const addQrcode = (overtime,number) => myAxios('/user/add_qrcode', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        overtime,
        number,
    }
});
/**
 * 删除二维码
 * @param qrcodeid
 * @returns {Promise<*|undefined>}
 */
export const deleteQrcode = (qrcodeid) => myAxios('/user/delete_qrcode', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        qrcodeid
    }
});

export const removeFile = (url, token) => myAxios('/user/remove_file', {
    method: 'post',
    params: {
        token,
    },
    data: {
        url
    }
});

/**
 * 获取注册页面信息
 * @param url
 * @returns {Promise<*|undefined>}
 */
export const getRegisterInfo = (qrid) => myAxios('/user/get_registerinfo', {
    method: 'post',
    data:{
        qrid
    }
});
export const checkQrcode = (qrid) => myAxios('/user/check_qrcode', {
    method: 'post',
    data:{
        qrid
    }
});
/**
 * 注册
 * @param formData
 * @returns {Promise<*|undefined>}
 */
export const register = (formData) => myAxios('/user/register', {
    method: 'post',
    data: formData
});

/**
 * 提现获取信息
 * @returns {Promise<*|undefined>}
 */
export const getDrawInfo = () => myAxios('/account/get_draw_info', {
    params:{
        token: getStore(TOKEN)
    }
});
/**
 * 提现
 * @param bankname
 * @param branchbank
 * @returns {Promise<*|undefined>}
 */
export const drawMoney = (formData) => myAxios('/account/draw_money', {
    method: 'post',
    params:{
        token: getStore(TOKEN)
    },
    data:formData
});
/**
 * 获取提现列表
 * @param status    0全部，1待审核，2待打款，3已打款，4未通过
 * @returns {Promise<*|undefined>}
 */
export const getDrawMoneyList = (status) => myAxios('/account/get_drawmoney_list', {
    method: 'post',
    params:{
        token: getStore(TOKEN)
    },
    data:{
        status
    }
});

/**
 * 线下充值
 * @param formData
 * @returns {Promise<*|undefined>}
 */
export const chargeMonney = (formData) => myAxios('/account/charge_monney', {
    method: 'post',
    params:{
        token: getStore(TOKEN)
    },
    data:formData
});
/**
 * 获取充值记录
 * @param status
 * @returns {Promise<*|undefined>}
 */
export const getChargeMoneyList = (status) => myAxios('/account/get_chargemoney_list', {
    method: 'post',
    params:{
        token: getStore(TOKEN)
    },
    data:{
        status
    }
});

/**
 * 查询保证金状态
 * 返回值 bailstatus   1:已缴纳   2.不足    3.退还中
 * @returns {Promise<*|undefined>}
 */
export const checkBail = () => myAxios('/account/check_bail', {
    params:{
        token: getStore(TOKEN)
    }
});
/**
 * 充值/退还 保证金
 * @param type  1:充值    2:退还
 * @param mount 金额
 * @returns {Promise<*|undefined>}
 */
export const chargeDrawBail = (type, mount) => myAxios('/account/charge_draw_bail', {
    method: 'post',
    params:{
        token: getStore(TOKEN)
    },
    data:{
        type,
        mount
    }
});




















