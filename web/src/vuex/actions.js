import {
    getUserBasicInfo,
    getCompanyMessage, getUserTotalInfo,
} from 'src/api/api'
import {
    SET_USER_INFO,
    SET_NOT_READ_COM_MSG,
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
}
