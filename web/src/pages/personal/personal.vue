<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        padding-bottom: 150px;

        .container-hd{
            position: relative;
            .banner {
                height: 290px;
                margin-bottom: 10px;

                .banner-img {
                    .wl(100%, 100%);
                }
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
                border-right: 2px solid @mainColor;
                border-bottom: 2px solid @mainColor;

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
        <section class="container-hd">
            <mt-swipe class="banner">
                <mt-swipe-item v-for="item in banner.personUrls" :key="item.SMid">
                    <img class="banner-img" v-lazy="item.SMurl" alt="">
                </mt-swipe-item>
            </mt-swipe>
            <router-link to="/setting" tag="img" class="go-setting" src="/static/images/setting.png" ></router-link>
        </section>


        <section class="user-info">
            <section class="user-img">
                <img v-lazy="userInfo.USheadimg" alt="">
            </section>

            <section class="user-info-detail">
                <p class="user-level">{{userInfo.USname}}</p>
                <p class="user-sale">销售量：<span class="user-sale-num">{{performance}}</span> 件</p>
            </section>
        </section>

        <ul class="function-panel">
            <li class="function-item" @click="goFunctionPage('/wallet')">
                <img src="/static/images/wallet.png" alt="">
                <span>我的钱包</span>
            </li>
            <li class="function-item" @click="goFunctionPage('/sale')">
                <img src="/static/images/sale.png" alt="">
                <span>我的销售</span>
            </li>
            <li class="function-item" @click="goFunctionPage('/channel')">
                <img src="/static/images/channel.png" alt="">
                <span>我的渠道</span>
            </li>
            <li class="function-item" @click="goFunctionPage('/mall')">
                <img src="/static/images/purchase.png" alt="">
                <span>我要进货</span>
            </li>
            <li class="function-item" @click="goFunctionPage('/mallOrder')">
                <img src="/static/images/order.png" alt="">
                <span>云仓订单</span>
            </li>
            <li class="function-item" @click="goFunctionPage('/authorization')">
                <img src="/static/images/authorization.png" alt="">
                <span>我的授权</span>
            </li>
            <li class="function-item" @click="goFunctionPage('/promotion')">
                <img src="/static/images/promotion.png" alt="">
                <span>我要推广</span>
            </li>
            <li class="function-item" @click="goFunctionPage('/integratedService')">
                <img src="/static/images/integrated_service.png" alt="">
                <span>综合业务</span>
            </li>
        </ul>

        <footer-guide></footer-guide>

    </div>
</template>

<script>
    import footerGuide from "src/components/footer/footerGuide"
    import {mapState,mapActions,mapMutations} from "vuex"
    import {getAccount} from "src/api/api"


    export default {
        name: "personal",

        data() {
            return {
                performance: 0
            }
        },

        computed:{
            ...mapState(['userInfo', 'banner']),
        },

        components: {
            footerGuide
        },

        methods: {
            goFunctionPage(path){
                this.$router.push(path);
            },
        },

        created(){
            let nowDate = new Date(),
                month = nowDate.getFullYear().toString();

            if(nowDate.getMonth() + 1 < 10){
                month += '0' + nowDate.getMonth() + 1;
            }else{
                month += nowDate.getMonth() + 1
            }
            getAccount(month).then(
                resData => {
                    if(resData){
                        this.performance = resData.data.performance;
                    }
                }
            )
        }
    }
</script>

