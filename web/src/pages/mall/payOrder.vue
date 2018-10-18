<style lang="less" scoped>
    @import "../../common/css/index";

    .pay-order-container {

        .choose-address {
            padding: 18px 36px 28px 30px;
            .fj();
            align-items: center;
            background: white;

            .choose-address-hd {
                .wl(24px, 35px);
            }
            .choose-address-ft {
                .wl(15px, 26px);

            }
        }

        .goods-list-container {
            box-shadow: 0px 3px 3px rgba(0, 0, 0, 0.16);
            margin-bottom: 10px;
            padding: 20px 20px 15px;
            background: white;

            .goods-list {
                border-bottom: 1px solid @grayBorderColor;

                .goods-item {
                    .fj();
                    margin-bottom: 10px;

                    .goods-img-wrap {
                        margin-right: 44px;
                        .wl(100px, 100px);

                        img {
                            .wl(100%, 100%);
                        }
                    }

                    .goods-item-description {
                        flex: 1;

                        .goods-name {
                            .fz(28px);

                        }
                        .goods-price {
                            text-align: right;
                            .sc(24px, @lightFontColor);
                            margin: 13px 0 10px;
                        }
                        .goods-shop-num {
                            text-align: right;
                            .sc(24px, @lightFontColor);
                        }
                    }

                }
            }

            .remark {
                .fj();
                padding: 11px 0;
                border-bottom: 1px solid @grayBorderColor;
                height: 32px;
                line-height: 32px;

                .remark-label {
                    color: #FC0000;
                    margin-right: 24px;
                }
                .remark-input {
                    flex: 1;
                    height: 32px;
                    line-height: 32px;
                    .fz(24px);
                }
            }

            .total-num {
                padding-top: 18px;
                text-align: right;
            }
        }

        .cell-list {
            margin-bottom: 10px;
            box-shadow: 0 3px 3px rgba(0, 0, 0, .16);
            padding: 20px;
            background: white;
            .fz(28px);

            .cell-item {
                .fj();
                padding: 10px 0;
                border-bottom: 1px solid @grayBorderColor;

                &:last-of-type{
                    border-bottom: none;
                }
            }
        }

        .confirm-pay-wrap{
            margin-top: 60px;
            margin-bottom: 186px;
            .fj(center);

            .confirm-pay-btn{
                .wl(600px, 90px);
                background: linear-gradient(180deg, @mainLightColor 0%, @mainColor 100%);
                .sc(38px, white);
                .fontc(80px);
                border: none;
                border-radius: 50px;
            }
        }

    }
</style>

<template>
    <section class="pay-order-container">
        <header-top title="结算" :showBack="true">
        </header-top>

        <section class="choose-address">
            <img class="choose-address-hd" src="/static/images/position.png" alt="">

            <section class="address-detail">
                <p class="row-one">
                    <span>xx</span>
                    <span>15500000000</span>
                </p>
                <p class="row-two">
                    浙江省 杭州市 江干区 九堡九润公寓1幢1单元1101
                </p>
            </section>

            <img class="choose-address-ft" src="/static/images/arrow.png" alt="">
        </section>


        <section class="goods-list-container">
            <ul class="goods-list">
                <li class="goods-item" v-for="item in 6">
                    <section class="goods-img-wrap">
                        <img src="/static/images/testbg.jpg" alt="">
                    </section>

                    <section class="goods-item-description">
                        <p class="goods-name">
                            纸尿裤
                        </p>
                        <p class="goods-price">
                            ￥216.00
                        </p>
                        <p class="goods-shop-num">
                            ×3
                        </p>
                    </section>
                </li>
            </ul>

            <section class="remark">
                <span class="remark-label">买家备注:</span>
                <input type="text" class="remark-input" placeholder="文化衫请备注尺码">
            </section>

            <p class="total-num">共几件商品</p>
        </section>

        <ul class="cell-list">
            <li class="cell-item">
                <div class="cell-left">商品金额</div>
                <div class="cell-right">￥100元</div>
            </li>
            <li class="cell-item">
                <div class="cell-left">快递费用</div>
                <div class="cell-right">￥100元</div>
            </li>
            <li class="cell-item">
                <div class="cell-left">合计需付</div>
                <div class="cell-right">￥100元</div>
            </li>
        </ul>

        <ul class="cell-list">
            <li class="cell-item">
                <div class="cell-left">可用贷款</div>
                <div class="cell-right">￥100元</div>
            </li>
            <li class="cell-item">
                <div class="cell-left">可用余额</div>
                <div class="cell-right">￥100元</div>
            </li>
        </ul>

        <section class="confirm-pay-wrap">
            <button class="confirm-pay-btn">
                确定下单
            </button>
        </section>
    </section>
</template>

<script>
    import BScroll from 'better-scroll'

    export default {
        name: "payOrder",

        data() {
            return {}
        },

        components: {},

        methods: {},

        mounted() {

        }
    }
</script>

