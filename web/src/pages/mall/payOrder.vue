<style lang="less" scoped>
    @import "../../common/css/index";

    .pay-order-container {
        .least-full-screen();
        padding-bottom: 100px;

        .choose-address {
            padding: 18px 36px 28px 30px;
            .fj();
            align-items: center;
            background: white;
            margin-bottom: 10px;

            .choose-address-hd {
                .wl(24px, 35px);
                margin-right: 18px;
            }

            .address-detail {
                flex: 1;

                .row-one {
                    margin-bottom: 10px;
                }
            }

            .no-address-tip {
                color: @mainColor;
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
                        .fjc();
                        .fz(26px);

                        .goods-name {
                            .fj();

                            .name {
                            }
                            .sku {
                                color: @lightFontColor;
                            }
                        }

                        .goods-num {
                            .fj();

                            .shop-num {
                                color: @lightFontColor;

                            }
                        }
                    }

                }
            }

            .remark {
                .fj();
                padding: 14px 0;
                border-bottom: 1px solid @grayBorderColor;
                /*height: 32px;*/
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

                &:last-of-type {
                    border-bottom: none;
                }
            }
        }

        .confirm-pay-wrap {
            margin-top: 60px;
            margin-bottom: 186px;
            .fj(center);

            .confirm-pay-btn {
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

        <router-link to="/addressList?isChoose=true" tag="section" class="choose-address">
            <img class="choose-address-hd" src="/static/images/position.png" alt="">

            <section v-if="defaultAddress" class="address-detail">
                <p class="row-one">
                    <span>{{defaultAddress.username}}</span>
                    <span>{{defaultAddress.userphonenum}}</span>
                </p>
                <p class="row-two">
                    {{defaultAddress.provincename}}-{{defaultAddress.cityname}}-{{defaultAddress.areaname}}
                    {{defaultAddress.details}}
                </p>
            </section>

            <section v-else class="no-address-tip">
                前往选择或新增地址
            </section>

            <img class="choose-address-ft" src="/static/images/arrow.png" alt="">
        </router-link>


        <section class="goods-list-container">
            <ul class="goods-list">
                <template v-for="product in cartList">
                    <li class="goods-item" v-for="cartItem in product.skulist">
                        <section class="goods-img-wrap">
                            <img :src="product.PRpic" alt="">
                        </section>

                        <section class="goods-item-description">
                            <p class="goods-name">
                                <span class="name">
                                    {{product.PRname}}
                                </span>
                                <span class="sku">
                                    {{`${cartItem.colorname} ${cartItem.sizename}`}}
                                </span>
                            </p>
                            <p class="goods-num">
                                <span class="price">
                                    ￥{{product.PRprice}}
                                </span>
                                <span class="shop-num">
                                    ×{{cartItem.number}}
                                </span>

                            </p>
                        </section>
                    </li>
                </template>

            </ul>

            <section class="remark">
                <span class="remark-label">买家备注:</span>
                <input type="text" v-model.trim="remark" class="remark-input" placeholder="文化衫请备注尺码">
            </section>

            <p class="total-num">共{{totalObj.totalNumber}}件商品</p>
        </section>

        <ul class="cell-list">
            <li class="cell-item">
                <div class="cell-left">商品金额</div>
                <div class="cell-right">￥{{totalObj.totalPrice}}元</div>
            </li>
            <li class="cell-item">
                <div class="cell-left">快递费用</div>
                <div class="cell-right">￥{{totalObj.expressMoney}}元</div>
            </li>
            <li class="cell-item">
                <div class="cell-left">合计需付</div>
                <div class="cell-right">￥{{totalObj.needPayMoney}}元</div>
            </li>
        </ul>

        <ul class="cell-list">
            <li class="cell-item">
                <div class="cell-left">可用余额</div>
                <div class="cell-right">￥{{userInfo.USmount}}元</div>
            </li>
        </ul>

        <section class="confirm-pay-wrap">
            <button class="confirm-pay-btn" @click="confirmPayOrder">
                确 定 下 单
            </button>
        </section>
    </section>
</template>

<script>
    import {mapState, mapGetters, mapActions} from "vuex"
    import {createOrder, getUserAddress} from "src/api/api"


    export default {
        name: "payOrder",

        data() {
            return {
                defaultAddress: null,
                cartList: [],
                remark: '', // 备注
            }
        },

        computed: {
            ...mapState(['userInfo']),

            totalObj() {
                let totalNumber = 0,
                    totalPrice = 0,
                    expressMoney = 0,
                    needPayMoney = 0;

                if (this.cartList.length == 1 && this.cartList[0].skulist.length == 1 && this.cartList[0].skulist[0].number == 1) {
                    expressMoney = this.cartList[0].PRlogisticsfee;
                }

                for (let i = 0; i < this.cartList.length; i++) {
                    let currentProduct = this.cartList[i];

                    for (let j = 0; j < currentProduct.skulist.length; j++) {
                        let currentCartItem = currentProduct.skulist[j];

                        totalNumber += currentCartItem.number;
                        totalPrice += currentCartItem.number * currentProduct.PRprice;
                    }
                }

                totalPrice = totalPrice.toFixed(2);

                needPayMoney = Number(expressMoney) + Number(totalPrice);

                return {
                    totalNumber,
                    totalPrice,
                    expressMoney,
                    needPayMoney,
                }
            },

        },

        components: {},

        methods: {
            ...mapActions(['getUserInfo']),
            async setDefaultAddress() {
                let resData = await getUserAddress(1, 0, '');

                if (resData) {
                    this.defaultAddress = resData.data;
                }
            },

            confirmPayOrder() {
                if (this.defaultAddress) {
                    this.$messagebox.confirm(`需支付${this.totalObj.needPayMoney}元,确认下单?`).then(
                        () => {
                            createOrder(this.defaultAddress.uaid, this.cartList,
                                this.remark, this.totalObj.expressMoney, this.totalObj.needPayMoney).then(
                                (resData) => {
                                    if (resData) {
                                        let {success, message} = resData;

                                        if (success) {
                                            this.$toast(message);
                                            this.$router.push({
                                                path: '/mall',
                                                // query:{
                                                //     goOrderList: true
                                                // }
                                            });
                                        } else {
                                            this.$messagebox('提示', '下单失败,请返回购物车再次选择商品结算!')
                                        }
                                    }
                                }
                            )
                        }
                    )

                } else {
                    this.$toast('请选择或新增地址!');
                }

            }
        },

        async mounted() {
            this.getUserInfo();
            this.setDefaultAddress();

            this.cartList = JSON.parse(this.$route.query.cartList);
        },

        created() {
            // console.log(this.$route);
        },
    }
</script>

