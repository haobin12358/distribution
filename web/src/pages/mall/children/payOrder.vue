<style lang="less" scoped>
    @import "~src/common/css/index";

    .pay-order-container{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: white;
        z-index: 10;

        .choose-address{
            padding: 18px 36px 28px 30px;
            .fj();
            align-items: center;

            .choose-address-hd{
                .wl(24px ,35px);
            }
            .choose-address-ft{
                .wl(15px ,26px);

            }
        }

    }
</style>

<template>
    <div class="pay-order-container">
        <header-top title="结算" showBack="true">
        </header-top>

        <section class="choose-address">
            <img class="choose-address-hd" src="/static/images/position.png" alt="">

            <section class="address-detail">
                <p class="address-detail"></p>
            </section>

            <img class="choose-address-ft" src="/static/images/arrow.png" alt="">
        </section>
        结算
    </div>
</template>

<script>
    export default {
        name: "payOrder",

        data() {
            return {}
        },

        components: {},

        methods: {},
    }
</script>

