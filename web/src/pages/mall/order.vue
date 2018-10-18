<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        min-height: 100vh;
        .nav-bar {
            .fj();
            background: white;

            .nav-bar-item {
                flex: 1;
                height: 80px;
                .fontc(80px);
                text-align: center;

                &.active {
                    border-bottom: 3px solid @mainColor;
                }
            }

        }

        .order-list {
            background: white;

            .order-item {
                padding: 16px 26px;
                margin-top: 10px;

                .order-item-header {
                    padding-bottom: 16px;
                    border-bottom: 1px solid @grayBorderColor;

                    .row-one {
                        margin-bottom: 4px;

                        .fj();

                        .no {

                        }

                        .status {
                            color: @mainColor;
                        }
                    }
                    .row-two {

                    }
                }

                .goods-list{
                    border-bottom: 1px solid @grayBorderColor;
                    .goods-item{
                        padding: 36px 0;
                        .fj();

                        .goods-img{
                            .wl(100px, 100px);
                            margin-right: 40px;

                            img{
                                .wl(100%, 100%);
                            }
                        }

                        .goods-description{
                            .fj();
                            flex-direction: column;
                            flex: 1;

                            .row-one{
                                .fj();

                                .goods-name{

                                }
                                .goods-price{
                                    color: @lightFontColor;
                                }
                            }

                            .row-two{
                                color: @lightFontColor;
                                text-align: right;
                            }
                        }

                    }
                }

                .order-item-total{
                    .fj(flex-end);
                    padding-top: 10px;

                    .total-num{
                        margin-right: 10px;
                    }
                    .total-price{

                    }
                }
            }

        }
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>
        <ul class="nav-bar">
            <li class="nav-bar-item active">
                全部(3)
            </li>
            <li class="nav-bar-item">
                代发货(1)
            </li>
            <li class="nav-bar-item">
                已发货(1)
            </li>
            <li class="nav-bar-item">
                已完成(1)
            </li>

        </ul>

        <ul class="order-list">
            <li class="order-item">
                <header class="order-item-header">
                    <p class="row-one">
                        <span class="no">编号：15574654156431231321</span>
                        <span class="status">已完成</span>
                    </p>
                    <p class="row-two">
                        时间：2017-08-19 15：15：23
                    </p>
                </header>

                <ul class="goods-list">
                    <li class="goods-item" v-for="item in 2">
                        <section class="goods-img">
                            <img src="/static/images/testbg.jpg" alt="">
                        </section>
                        <section class="goods-description">
                            <p class="row-one">
                                <span class="goods-name">蓓莉纸尿裤拉拉裤游泳裤</span>
                                <span class="goods-price">￥216.00</span>
                            </p>
                            <p class="row-two">
                                ×3
                            </p>
                        </section>
                    </li>
                </ul>
                <footer class="order-item-total">
                    <span class="total-num">共3商品</span>
                    <span class="total-price">价值:￥644</span>
                </footer>
            </li>
        </ul>
    </div>
</template>

<script>
    export default {
        name: "order",

        data() {
            return {}
        },

        components: {},

        methods: {},
    }
</script>

