<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();
        .fjc();

        .main-content{
            flex: 1;
            .fjc();

            .tip{
                padding: 0 45px;
                margin-top: 57px;
                text-align: center;
                .sc(30px, black);
            }
        }

    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <section class="main-content">
            <p class="tip">
                绑定微信并关注公众号后，可以及时接收最近订单信息，奖金信息，新代理信息等。
            </p>

            <section class="my-confirm-btn-wrap" style="margin: 0 0 80px;">
                <button class="my-confirm-btn">绑 定</button>
            </section>
        </section>
    </div>
</template>

<script>
    export default {
        name: "linkWechat",

        data() {
            return {}
        },

        components: {},

        computed: {},

        methods: {},

        created() {
        },
    }
</script>

