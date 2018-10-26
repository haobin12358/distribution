import {
    SAVE_READING_MESSAGE,
    SET_AGENT_MESSAGE,
    SET_COMPANY_MESSAGE,
    SET_USER_INFO,
    SET_SHOW_AGENT,
    SET_NOT_READ_COM_MSG,
    ADD_CART,
    REDUCE_CART,
    INIT_CART,
} from './mutation-types'
import {TOKEN, USER_INFO, NOT_READ_COM_MSGS, CART_LIST} from "src/common/js/const"
import {setStore, getStore} from "src/common/js/mUtils"

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
        setStore(USER_INFO, payload);
        state.userInfo = payload;
    },
    [SET_SHOW_AGENT](state, payload) {
        state.showAgent = payload;
    },
    [SET_NOT_READ_COM_MSG](state, payload) {
        setStore(NOT_READ_COM_MSGS, payload);
        state.notReadComMsg = payload;
    },
    [ADD_CART](state, payload) {
        let changeItem = state.cartList.find(item => item.PRid == payload.PRid);

        if (changeItem) {
            changeItem.PRnum++;
        } else {
            payload.PRnum = 1;
            state.cartList = [...state.cartList, payload];
        }

        state.cartList = state.cartList.concat();
        setStore(CART_LIST, state.cartList);
    },
    [REDUCE_CART](state, payload) {
        let cart = state.cartList.concat();
        let changeItem = state.cartList.find(item => item.PRid == payload.PRid);

        if (changeItem) {
            if (changeItem.PRnum > 0) {
                changeItem.PRnum--;
            }
        }

        state.cartList = state.cartList.concat();
        setStore(CART_LIST, state.cartList);
    },
    [INIT_CART](state, payload) {
        let cartListSto = getStore(CART_LIST);

        if(cartListSto){
            state.cartList =JSON.parse(cartListSto);

        }
    },


}
