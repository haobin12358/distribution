<style lang="less" scoped>
    @import "../../common/css/index";

    .container{
        .least-full-screen();

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
            <router-link tag="li" to="/changeHeadImg" class="cell">
                <img src="/static/images/head_img.png" alt="" class="cell-icon">

                <span class="cell-title">更换头像</span>
                <img src="/static/images/arrow.png" alt="" class="cell-ft">
            </router-link>
            <router-link tag="li" to="/changePassword" class="cell">
                <img src="/static/images/password.png" alt="" class="cell-icon">

                <span class="cell-title">修改密码</span>
                <img src="/static/images/arrow.png" alt="" class="cell-ft">
            </router-link>
            <router-link tag="li" to="/addressList" class="cell">
                <img src="/static/images/position.png" alt="" class="cell-icon">

                <span class="cell-title">我的地址</span>
                <img src="/static/images/arrow.png" alt="" class="cell-ft">
            </router-link>

        </ul>
    </div>
</template>

<script>
    export default {
        name: "setting",

        data() {
            return {}
        },

        components: {},

        methods: {},
    }
</script>

