<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();
        padding-bottom: 50px;

        .banner {
            height: 290px;
            position: relative;
            margin-bottom: 10px;

            .banner-img {
                .wl(100%, 100%);
            }
        }

        .cell-wrap {
            padding: 0 20px 0;
            .bgw();

            .cell {
                padding: 25px 0;
                .fj();
                align-items: center;
                border-bottom: 1px solid @grayBorderColor;

                &:last-child {
                    border-bottom: none;
                }

                .cell-icon {
                    .wl(47px, 47px);
                    margin-right: 20px;
                }



                .cell-title {
                    flex: 1;
                    .fz(32px);
                }

                .cell-ft {
                    .wl(18px, 31px);

                }

            }
        }

    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <mt-swipe class="banner">
            <mt-swipe-item v-for="item in 5" :key="item">
                <img class="banner-img" src="/static/images/testbg.jpg" alt="">
            </mt-swipe-item>
        </mt-swipe>

        <ul class="cell-wrap">
            <router-link tag="li" to="/setting" class="cell">
                <img src="/static/images/head_img.png" alt="" class="cell-icon">

                <span class="cell-title">个人信息</span>
                <img src="/static/images/arrow.png" alt="" class="cell-ft">
            </router-link>

            <router-link tag="li" to="/message" class="cell">
                <img src="/static/images/message.png" alt="" class="cell-icon">

                <span class="cell-title">我的消息</span>
                <img src="/static/images/arrow.png" alt="" class="cell-ft">
            </router-link>

            <router-link tag="li" to="/protocol" class="cell">
                <img src="/static/images/protocol.png" alt="" class="cell-icon">

                <span class="cell-title">代理协议</span>
                <img src="/static/images/arrow.png" alt="" class="cell-ft">
            </router-link>

            <router-link tag="li" to="/linkWechat" class="cell">
                <img src="/static/images/wechat.png" alt="" class="cell-icon">

                <span class="cell-title">绑定微信</span>
                <img src="/static/images/arrow.png" alt="" class="cell-ft">
            </router-link>

            <router-link tag="li" to="/feedback" class="cell">
                <img src="/static/images/feedback.png" alt="" class="cell-icon">

                <span class="cell-title">问题反馈</span>
                <img src="/static/images/arrow.png" alt="" class="cell-ft">
            </router-link>
        </ul>

        <section class="my-confirm-btn-wrap">
            <button class="my-confirm-btn disabled" @click="doLogout">退 出 登 录</button>
        </section>
    </div>
</template>

<script>
    import {setStore, getStore} from "src/common/js/mUtils"
    import {TOKEN} from "src/common/js/const"

    export default {
        name: "integratedService",

        data() {
            return {}
        },

        components: {},

        methods: {
            doLogout(){
                this.$messagebox.confirm('确定退出系统?').then(
                    action => {
                        localStorage.clear();   // todo 不应该请调所有缓存
                        this.$router.replace('/login');
                    }
                ).catch(evt=>{})
            }
        },


    }
</script>

