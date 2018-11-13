import {
    getUserBasicInfo,
    getCompanyMessage,
    getUserTotalInfo,
    getSowingMap,
} from 'src/api/api'
import {
    SET_USER_INFO,
    SET_NOT_READ_COM_MSG,
    SET_BANNER_IMGS,
} from "./mutation-types"

export default {
    async getUserInfo({commit, state}) {
        let {data} = await getUserTotalInfo();

        if (data) {
            commit(SET_USER_INFO, data);
        }
    },
    async setNotReadMsgNum({commit, state}){
        let {notread} =await getCompanyMessage(1);

        commit(SET_NOT_READ_COM_MSG, notread);
    },
    async getSowingMap({commit, state}){
        let {data} =await getSowingMap();

        commit(SET_BANNER_IMGS, data);
    },

}
