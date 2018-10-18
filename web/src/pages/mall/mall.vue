<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        padding-bottom: 100px;

        #go-order-img {
            .wl(33px, 27px);
        }

        .pay-order {
            width: 129px;
            height: 36px;
            border: 1px solid rgba(255, 255, 255, 1);
            border-radius: 20px;
            .fontc(36px);
            .sc(24px, white);
            background: @mainColor;
        }

        .banner {
            height: 180px;
            margin-bottom: 10px;

            img {
                width: 100%;
                height: 100%;
            }
        }

        .nav-wrap {
            .nav-list-parent {
                background: white;
                overflow-x: scroll;
                white-space: nowrap;

                .nav-item {
                    height: 80px;
                    display: inline-block;
                    padding: 0 25px;
                    .fontc(80px);

                    &.active {
                        border-bottom: 3px solid @mainColor;
                    }
                }
            }
            .nav-list-children {
                height: 80px;
                overflow-x: scroll;
                .fj(flex-start);
                align-items: center;
                flex-wrap: nowrap;

                .pillow-item {
                    /*line-height: 80px;*/
                    /*display: inline-block;*/
                    margin-right: 50px;
                    border: 1px solid rgba(110, 171, 184, 1);
                    padding: 4px 23px;
                    border-radius: 30px;
                    white-space: nowrap;

                    &:first-of-type {
                        margin-left: 42px;
                    }
                    &:last-of-type {
                        margin-right: 42px;
                    }
                }

                .pillow-item-tail {
                    flex: 42px;
                    .wl(42px, 10px);
                }

            }
        }

        .goods-list {
            padding: 0 10px;
            background: white;

            .goods-item {
                padding: 35px 2px 32px 16px;
                border-bottom: 1px solid #DBDBDB;
                .fj();

                &:last-child {
                    border-bottom: 0;
                }

                .goods-img {
                    margin-right: 40px;
                    .wl(100px, 100px);

                    img {
                        .wl(100%, 100%);
                    }
                }

                .goods-description {
                    flex: 1;
                    .fj();
                    flex-direction: column;
                    .goods-description-header {
                        .fz(28px);

                    }
                    .goods-description-content {
                        .fj();

                        .goods-description-price {

                            .current-price {
                                margin-right: 20px;
                                color: #FC0000;

                            }
                            .original-price {
                                color: black;
                                text-decoration: line-through;

                            }
                        }

                    }
                }
            }
        }
    }
</style>

<template>
    <div class="container">
        <header-top :title="'云仓'">
            <section slot="left" @click="goOrder">
                <img id="go-order-img" src="/static/images/myOrder.png" alt="">
            </section>
            <section slot="right">
                <button class="pay-order" @click="goPayOrder">结算</button>
            </section>
        </header-top>

        <section class="banner">
            <img src="/static/images/testbg.jpg" alt="">
        </section>

        <section class="nav-wrap">
            <ul class="nav-list-parent">
                <li class="nav-item active">一级asas</li>
                <li class="nav-item">一级ssss</li>
                <li class="nav-item">一级sddsds</li>
                <li class="nav-item">一级sd</li>
                <li class="nav-item">一级dsd</li>
                <li class="nav-item">一级</li>
                <li class="nav-item">一级</li>
                <li class="nav-item">一级</li>

            </ul>
            <ul class="nav-list-children">
                <li class="pillow-item">2级xx</li>
                <li class="pillow-item">2级</li>
                <li class="pillow-item">2级asdasdxx</li>
                <li class="pillow-item">2级asdasdxx</li>
                <li class="pillow-item">2级asdasdxx</li>
                <li class="pillow-item">2级</li>
                <li class="pillow-item">2级</li>

                <li class="pillow-item-tail"></li>
            </ul>
        </section>

        <ul class="goods-list">
            <li class="goods-item" v-for="item in 6">
                <section class="goods-img">
                    <img src="/static/images/testbg.jpg" alt="">
                </section>
                <section class="goods-description">
                    <header class="goods-description-header">
                        蓓莉纸尿裤（M码） （36片*4包）
                    </header>
                    <section class="goods-description-content">
                        <p class="goods-description-price">
                            <span class="current-price">￥216.00</span>
                            <span class="original-price">￥236.00</span>
                        </p>

                        <buy-cart></buy-cart>
                    </section>

                </section>
            </li>
        </ul>

        <footer-guide></footer-guide>
    </div>
</template>

<script>
    import {Toast} from "mint-ui"
    import footerGuide from "src/components/footer/footerGuide"
    import buyCart from "src/components/common/buyCart"

    export default {
        name: "mall",

        data() {
            return {}
        },

        components: {
            buyCart,
            footerGuide,
        },

        methods: {
            goOrder() {
                this.$router.push('/mallOrder');
            },
            goPayOrder() {
                this.$router.push('/payOrder');
            }
        },

        mounted() {

            // this.$toast({
            //   message: 'success',
            //   iconClass: 'm-toast-success',
            //   duration: 30000
            // })
        }
    }
</script>

