<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        padding-bottom: 100px;

        .banner {
            height: 290px;
            position: relative;
            margin-bottom: 10px;

            .banner-img {
                .wl(100%, 100%);
            }

            .go-setting {
                position: absolute;
                .wl(49px, 49px);
                top: 22px;
                right: 22px;
            }
        }

        .user-info {
            padding: 11px 26px;
            .fj();
            align-items: center;
            background: white;
            margin-bottom: 10px;

            .user-img {
                .wl(113px, 113px);
                margin-right: 32px;

                img {
                    .wl(100%, 100%);
                    border: 2px solid @mainColor;
                    border-radius: 50%;
                    box-sizing: border-box;
                }
            }

            .user-info-detail {
                flex: 1;

                .user-sale {
                    .user-sale-num {
                        color: #f76714;
                    }

                }
            }
        }

        .function-panel {
            display: flex;
            flex-wrap: wrap;
            background: white;

            .function-item {
                .wl(250px, 250px);
                background: white;
                box-sizing: border-box;
                .fj();
                flex-direction: column;
                align-items: center;
                padding: 30px 0 20px;
                border-right: 1px solid @mainColor;
                border-bottom: 1px solid @mainColor;

                img {
                    .wl(150px, 150px);
                }

                &:nth-child(3n) {
                    border-right: none;

                }

                &:nth-child(8) {
                    border-bottom: none;

                }
                &:nth-child(7) {
                    border-bottom: none;

                }
            }
        }

    }
</style>

<template>
    <div class="container">
        <mt-swipe class="banner">
            <mt-swipe-item v-for="item in 5" :key="item">
                <img class="banner-img" src="/static/images/testbg.jpg" alt="">
            </mt-swipe-item>
            <img class="go-setting" src="/static/images/setting.png" alt="">
        </mt-swipe>

        <section class="user-info">
            <section class="user-img">
                <img src="/static/images/testbg.jpg" alt="">
            </section>

            <section class="user-info-detail">
                <p class="user-level">{{userInfo.USname}}</p>
                <p class="user-sale">销售量：<span class="user-sale-num">todo</span> 件</p>
            </section>
        </section>

        <ul class="function-panel">

            <router-link tag="li" class="function-item" to="/wallet">
                <img src="/static/images/wallet.png" alt="">
                <span>我的钱包</span>
            </router-link>
            <router-link tag="li" class="function-item" to="/sale">
                <img src="/static/images/sale.png" alt="">
                <span>我的销售</span>
            </router-link>
            <router-link tag="li" class="function-item" to="/channel">
                <img src="/static/images/channel.png" alt="">
                <span>我的渠道</span>
            </router-link>
            <router-link tag="li" class="function-item" to="/mall">
                <img src="/static/images/purchase.png" alt="">
                <span>我要进货</span>
            </router-link>
            <router-link tag="li" class="function-item" to="/mallOrder">
                <img src="/static/images/order.png" alt="">
                <span>云仓订单</span>
            </router-link>
            <router-link tag="li" class="function-item" to="/authorization">
                <img src="/static/images/authorization.png" alt="">
                <span>我的授权</span>
            </router-link>
            <router-link tag="li" class="function-item" to="/promotion">
                <img src="/static/images/promotion.png" alt="">
                <span>我要推广</span>
            </router-link>
            <router-link tag="li" class="function-item" to="/integratedService">
                <img src="/static/images/integrated_service.png" alt="">
                <span>综合业务</span>
            </router-link>

        </ul>

        <footer-guide></footer-guide>

    </div>
</template>

<script>
    import footerGuide from "src/components/footer/footerGuide"
    import {mapState,mapActions,mapMutations} from "vuex"
    import {setStore, getStore} from "src/common/js/mUtils"
    import {TOKEN,USER_INFO} from "src/common/js/const"

    export default {
        name: "personal",

        data() {
            return {}
        },

        computed:{
            ...mapState(['userInfo']),
            // userInfo(){
            //     let userInfoState = this.$store.state.userInfo;
            //
            //     if(!Object.keys(userInfoState).length){
            //         let userInfoSto = getStore(USER_INFO);
            //
            //         if(userInfoSto){
            //             userInfoSto = JSON.parse(userInfoSto);
            //             this.setUserInfo(userInfoSto);
            //             return userInfoSto;
            //         }
            //     }else{
            //         return userInfoState;
            //     }
            // }
        },

        components: {
            footerGuide
        },

        methods: {
            ...mapMutations({
                setUserInfo: 'SET_USER_INFO'
            })

        },

        created(){
        }
    }
</script>

