import {
    SAVE_READING_MESSAGE,
    SET_AGENT_MESSAGE,
    SET_COMPANY_MESSAGE,
    SET_USER_INFO,
    INIT_USER_INFO,
    SET_SHOW_AGENT,
    SET_NOT_READ_COM_MSG,
    ADD_CART,
    REDUCE_CART,
    INIT_CART,
    CLEAR_CART,
    SET_CART,
    SET_CHOOSE_ADDRESS,
    INIT_ADD_TEN_CART_TIP,
    SET_ADD_TEN_CART_TIP,
    SET_BANNER_IMGS,
} from './mutation-types'
import {TOKEN, USER_INFO, NOT_READ_COM_MSGS, CART_LIST, ADD_TEN_CART_TIP} from "src/common/js/const"
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
    [INIT_USER_INFO](state, payload) {
        state.userInfo = JSON.parse(getStore(USER_INFO));
    },
    [SET_SHOW_AGENT](state, payload) {
        state.showAgent = payload;
    },
    [SET_NOT_READ_COM_MSG](state, payload) {
        setStore(NOT_READ_COM_MSGS, payload);
        state.notReadComMsg = payload;
    },
    [ADD_CART](state, payload) {
        let changeItem = state.cartList.find(item => item.PRid == payload.product.PRid);

        if (changeItem) {
            changeItem.PRnum += payload.num;
        } else {
            payload.product.PRnum = payload.num;
            state.cartList = [...state.cartList, payload.product];
        }

        state.cartList = state.cartList.concat();
        setStore(CART_LIST, state.cartList);
    },
    [REDUCE_CART](state, payload) {
        let cart = state.cartList.concat();
        let reduceIndex = 0;
        let changeItem = state.cartList.find((item, index) => {
            if (item.PRid == payload.PRid) {
                reduceIndex = index;
                return true;
            }
        });

        if (changeItem) {
            if (changeItem.PRnum > 1) {
                changeItem.PRnum--;
            }
            if (changeItem.PRnum == 1) {
                state.cartList.splice(reduceIndex, 1);
            }
        }

        // state.cartList = state.cartList.concat();
        setStore(CART_LIST, state.cartList);
    },
    [INIT_CART](state, payload) {
        let cartListSto = getStore(CART_LIST);

        if (cartListSto) {
            state.cartList = JSON.parse(cartListSto);

        }
    },
    [CLEAR_CART](state, payload) {
        state.cartList = [];
        setStore(CART_LIST, state.cartList);
    },
    [SET_CART](state, payload) {
        state.cartList = payload;
        setStore(CART_LIST, state.cartList);
    },

    [SET_CHOOSE_ADDRESS](state, payload) {
        state.chooseAddress = payload || null;
    },

    [SET_ADD_TEN_CART_TIP](state, payload) {
        state.addTenCartTip = payload;

        // console.log(state.addTenCartTip);

        setStore(ADD_TEN_CART_TIP, state.addTenCartTip);

        // console.log(getStore(ADD_TEN_CART_TIP));
    },
    [INIT_ADD_TEN_CART_TIP](state, payload) {
        let addTenCartTip = getStore(ADD_TEN_CART_TIP);

        if (addTenCartTip === null) {
            state.addTenCartTip = true;
        }else{
            state.addTenCartTip = JSON.parse(addTenCartTip) ? true : false;
        }
    },

    [SET_BANNER_IMGS](state, payload){
        state.banner = payload;
    }


}
