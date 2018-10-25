import axios from "axios"
import {Indicator, Toast} from "mint-ui"
import {getStore} from "src/common/js/mUtils"
import {TOKEN} from "src/common/js/const"

const debug = false;
const title = debug ? 'https://dsn.apizza.net/mock/60c954072cfff536376e5acb0392c590' : 'http://112.74.175.144:7444';

const myAxios = async (url, {params, data, method = 'get', showIndicator = true}) => {
    if (showIndicator) {
        Indicator.open({text: '加载中...', spinnerType: 'fading-circle'});
    }

    let res = await axios({
        baseURL: '/api',    //todo 代理
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

    if (res.status == 200) {
        if (res.data.status == 200) {
            return res.data.data;
        } else {
            Toast(res.data.message);
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
export const findBackPwd = (usphonenum,iccode,newpassword) => myAxios('/user/findback_pwd', {
    method: 'post',
    data: {
        usphonenum,
        iccode,
        newpassword
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
    params: {
        token: getStore(TOKEN),
        messageid
    }
});









