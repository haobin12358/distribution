<style lang="less" scoped>
    @import "../../common/css/index";

    .pay-order-container {
        .least-full-screen();

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
                <li class="goods-item" v-for="item in usefulCartList">
                    <section class="goods-img-wrap">
                        <img :src="item.PRpic" alt="">
                    </section>

                    <section class="goods-item-description">
                        <p class="goods-name">
                            {{item.PRname}}
                        </p>
                        <p class="goods-price">
                            ￥{{item.PRprice}}
                        </p>
                        <p class="goods-shop-num">
                            ×{{item.PRnum}}
                        </p>
                    </section>
                </li>
            </ul>

            <section class="remark">
                <span class="remark-label">买家备注:</span>
                <input type="text" v-model="remark" class="remark-input" placeholder="文化衫请备注尺码">
            </section>

            <p class="total-num">共几件商品</p>
        </section>

        <ul class="cell-list">
            <li class="cell-item">
                <div class="cell-left">商品金额</div>
                <div class="cell-right">￥{{cartTotalPrice}}元</div>
            </li>
            <li class="cell-item">
                <div class="cell-left">快递费用</div>
                <div class="cell-right">￥{{payDeliverFee}}元</div>
            </li>
            <li class="cell-item">
                <div class="cell-left">合计需付</div>
                <div class="cell-right">￥{{needPayAmount}}元</div>
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
                remark: '', // 备注
            }
        },

        computed: {
            ...mapState(['userInfo']),
            ...mapGetters(['usefulCartList', 'cartTotalPrice', 'payDeliverFee']),
            needPayAmount(){
                if(this.usefulCartList.length == 1 && this.usefulCartList[0].PRnum == 1){
                    return this.cartTotalPrice + this.usefulCartList[0].PRlogisticsfee;
                }else{
                    return this.cartTotalPrice;
                }
            }
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
                    this.$messagebox.confirm(`需支付${this.needPayAmount}元,确认下单?`).then(
                        () => {
                            createOrder(this.defaultAddress.uaid, this.usefulCartList,
                                this.remark, this.payDeliverFee, this.needPayAmount).then(
                                (resData) => {
                                    if (resData) {
                                        let {success, message, data: newCartList} = resData;

                                        if (success) {
                                            this.$toast(message);
                                            this.$store.commit('CLEAR_CART');
                                            //  更新账户余额
                                            this.getUserInfo();

                                            this.$router.back();
                                        } else {
                                            this.$messagebox('提示', '商品价格或运费有变动,下单失败,数据已更新,请再次确认下单!')
                                            this.$store.commit('SET_CART', newCartList);
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
            this.setDefaultAddress();
        }
    }
</script>

