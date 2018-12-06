import axios from "axios"
import {Indicator, Toast, MessageBox} from "mint-ui"
import {getStore, setStore} from "src/common/js/mUtils"
import {TOKEN} from "src/common/js/const"

const debug = false;
export const title = debug ? 'https://dsn.apizza.net/mock/60c954072cfff536376e5acb0392c590' : 'https://www.beiliyuncang.com/apis';

const myAxios = async (url, {params, data, method = 'get', showIndicator = true, showTypeIsMessage = false}) => {
    if (showIndicator) {
        Indicator.open({text: '加载中...', spinnerType: 'fading-circle'});
    }

    let res = await axios({
        baseURL: title,
        method: method,
        url: url,
        params: params,
        data: data,
    }).catch(
        evt => {
            if (showIndicator) {
                Indicator.close();
            }

            if (showTypeIsMessage) {
                MessageBox.alert('服务器忙!');
            } else {
                Toast('服务器忙!');
            }
        }
    )

    if (showIndicator) {
        Indicator.close();
    }

    if (res && res.status == 200) {
        if (res.data.status == 200) {
            return res.data;
        } else {
            if (showTypeIsMessage) {
                MessageBox.alert(res.data.message);
            } else {
                Toast(res.data.message);
            }

            if (res.data.status == 405 && res.data.status_code == 405003) {
                location.href = location.origin
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
export const getProductList = (PAtype, PAid, PRstatus, page_num, page_size = 10, PRname = '') => myAxios('/product/get_product_list', {
    showIndicator: false,
    params: {
        PAtype,
        PAid,
        page_size,
        page_num,
        PRstatus,
        PRname,
    }
});
/**
 * 获取商品详情
 * @param prid
 * @returns {Promise<*|undefined>}
 */
export const getProductDetails = (prid) => myAxios('/product/get_product_details', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        prid
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
 * 取消订单
 * @param oisn
 * @returns {Promise<*|undefined|void>}
 */
export const cancelOrder = (oisn) => myAxios('/order/cancel_order', {
    method: 'post',
    params: {
        token: getStore(TOKEN),
    },
    data: {
        oisn
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
    showIndicator: false,
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
export const getDirectagent = (page_num ,page_size = 10) => myAxios('/account/get_directagent', {
    params: {
        token: getStore(TOKEN),
        page_size,
        page_num,
    }
});
/**
 * 获取所有分销商代理
 * @returns {Promise<*|undefined>}
 */
export const getDistribute = (page_num ,page_size = 10) => myAxios('/account/get_distribute', {
    params: {
        token: getStore(TOKEN),
        page_size,
        page_num,
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
export const addQrcode = (overtime, number) => myAxios('/user/add_qrcode', {
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
    showIndicator: false,
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
    data: {
        qrid
    }
});
export const checkQrcode = (qrid) => myAxios('/user/check_qrcode', {
    method: 'post',
    data: {
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
    params: {
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
    params: {
        token: getStore(TOKEN)
    },
    data: formData
});
/**
 * 获取提现列表
 * @param status    0全部，1待审核，2待打款，3已打款，4未通过
 * @returns {Promise<*|undefined>}
 */
export const getDrawMoneyList = (status) => myAxios('/account/get_drawmoney_list', {
    method: 'post',
    params: {
        token: getStore(TOKEN)
    },
    data: {
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
    params: {
        token: getStore(TOKEN)
    },
    data: formData
});
/**
 * 获取充值记录
 * @param status
 * @returns {Promise<*|undefined>}
 */
export const getChargeMoneyList = (status) => myAxios('/account/get_chargemoney_list', {
    method: 'post',
    params: {
        token: getStore(TOKEN)
    },
    data: {
        status
    }
});

/**
 * 查询保证金状态
 * 返回值 bailstatus   1:已缴纳   2.不足    3.退还中
 * @returns {Promise<*|undefined>}
 */
export const checkBail = () => myAxios('/account/check_bail', {
    params: {
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
    params: {
        token: getStore(TOKEN)
    },
    data: {
        type,
        mount
    }
});

export const getMoneyRecord = () => myAxios('/account/get_moneyrecord', {
    params: {
        token: getStore(TOKEN)
    },
});

export const checkOpenid = () => myAxios('/user/check_openid', {
    params: {
        token: getStore(TOKEN)
    },
});

export const weixinPay = (amount) => myAxios('/account/weixin_pay', {
    method: 'post',
    data: {
        amount
    },
    params: {
        token: getStore(TOKEN)
    },
});

export const addComments = (CMcontent) => myAxios('/mycenter/add_comments', {
    method: 'post',
    data: {
        CMcontent
    },
    params: {
        token: getStore(TOKEN)
    },
});

export const getSowingMap = () => myAxios('/product/get_sowingmap', {
    params: {
        token: getStore(TOKEN)
    },
});

export const getAuthorization = () => myAxios('/user/get_authorization', {
    params: {
        token: getStore(TOKEN)
    },
});

//  购物车
export const addShoppingCart = (prid, sku, number) => myAxios('/product/add_shoppingcart', {
    showTypeIsMessage: true,
    method: 'post',
    data: {
        prid,
        "psid": sku.PSid,
        "colorid": sku.colorid,
        "colorname": sku.colorname,
        "sizeid": sku.sizeid,
        "sizename": sku.sizename,
        number
    },
    params: {
        token: getStore(TOKEN)
    },
});
export const getShoppingCart = () => myAxios('/product/get_shoppingcart', {
    params: {
        token: getStore(TOKEN)
    },
});
export const updateShoppingCartNumber = (psid, number) => myAxios('/product/update_shoppingcart_number', {
    method: 'post',
    params: {
        token: getStore(TOKEN)
    },
    data: {
        psid,
        number,
    }
});
export const deleteShoppingCart = (scidlist) => myAxios('/product/delete_shoppingcart_sku', {
    method: 'post',
    params: {
        token: getStore(TOKEN)
    },
    data: {
        scidlist
    }
});






















