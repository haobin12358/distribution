<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();

        .form-container {
            margin-top: 10px;
            .bs(0, 3px, 6px);
            padding: 20px;
            .bgw();

            .form-item {
            }


        }

        .confirm-btn-wrap {
            margin-top: 343px;
            .fj(center);

            .confirm-btn{
                .wl(600px, 90px);
                .fontc(90px);
                font-weight: bold;
                background: linear-gradient(180deg, @mainLightColor 0%, @mainColor 100%);
                .sc(38px, white);
                border-radius: 50px;

            }

        }
    }
</style>

<template>
    <div class="container">
        <header-top :title="$route.meta.title" :show-back="true">
            <section slot="right">
                <router-link to="/withdrawCashRecord" tag="img" src="/static/images/myOrder.png"
                             class="my-order-img"></router-link>
            </section>
        </header-top>

        <section class="form-container">
            <mt-field class="form-item" label="银行名称" placeholder="请输入银行名称"></mt-field>
            <mt-field class="form-item" label="支行名称" placeholder="请输入支行名称" type="email"></mt-field>
            <mt-field class="form-item" label="开户姓名" placeholder="请输入开户姓名" type="password"></mt-field>
            <mt-field class="form-item" label="卡号" placeholder="请输入卡号" type="password"></mt-field>
            <mt-field class="form-item" label="金额" placeholder="请输入金额" type="password"></mt-field>
        </section>

        <section class="confirm-btn-wrap">
            <button class="confirm-btn">确 认 提 现</button>
        </section>

    </div>
</template>

<script>
    export default {
        name: "withdrawCash",

        data() {
            return {}
        },

        components: {},

        methods: {},
    }
</script>

