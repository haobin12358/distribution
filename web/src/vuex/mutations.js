import {
    SAVE_READING_MESSAGE,
    SET_AGENT_MESSAGE,
    SET_COMPANY_MESSAGE,
    SET_USER_INFO
} from './mutation-types'

export default {
    [SAVE_READING_MESSAGE](state, msg) {
        state.readingMessage = msg;
    },
    [SET_AGENT_MESSAGE](state, msgs) {
        state.agentMessages = msgs;
    },
    [SET_COMPANY_MESSAGE](state, msgs) {
        state.companyMessages = msgs;
    },
    [SET_USER_INFO](state, payload) {
        state.userInfo = payload;
    },

}
