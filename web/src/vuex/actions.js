import {
    getUserBasicInfo
} from 'src/api/api'
import {
    SET_USER_INFO
} from "./mutation-types"
import {setStore, getStore} from "src/common/js/mUtils"
import {TOKEN,USER_INFO} from "src/common/js/const"

export default {
    async getUserInfo({commit, state}) {
        let data = await getUserBasicInfo();

        if (data) {
            console.log('[getuserinfo]');
            setStore(USER_INFO, data);
            commit(SET_USER_INFO, data);
        }
    }
}
