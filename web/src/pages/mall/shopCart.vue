<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();
        padding-bottom: 200px;

        .shop-cart-group-list {
            padding: 40px 24px;

            .shop-cart-group {
                border-radius: 20px;
                .bs(20px, 5px, 6px);
                .bgw();

                .shop-cart-item {
                    padding: 30px 20px 0 20px;
                    .fj();
                    align-items: center;

                    &:last-child {
                        padding-bottom: 30px;
                    }

                    .item-radio-section {
                        padding: 0 20px;
                        height: 153px;
                        line-height: 153px;

                        img {
                            .wl(40px, 40px);
                        }

                    }
                    .item-img-section {
                        margin-right: 30px;
                        .wl(153px, 153px);

                        img {
                            .wl(100%, 100%);
                        }
                    }
                    .item-detail-section {
                        flex: 1;
                        font-size: 28px;

                        .fjc();

                        .right-hd {
                            color: @333;
                        }
                        .right-bd {
                            .fj();
                            margin: 10px 0;

                            .sku {
                                padding: 4px 10px;
                                .sc(24px, @666);
                                background: #e9e9e9;
                                border-radius: 10px;
                            }

                            .status {
                                color: red;
                            }
                        }
                        .right-ft {
                            .fj();
                            align-items: center;

                            .price {
                                color: @moneyColor;
                            }
                        }
                    }

                }
            }
        }

        .pay-order-block {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            padding: 20px 35px;
            box-sizing: border-box;
            .bgw();

            .fj();
            align-items: center;

            .pay-order-left {
                .fj();

                .img-check-all {
                    .wl(40px, 40px);
                    margin-right: 10px;
                }

                .label-check-all {
                    .fz(26px);
                    line-height: 36px;
                }

            }
            .pay-order-right {
                .fj();
                align-items: center;

                .total-block {
                    margin-right: 16px;

                    .label {
                        .sc(30px, @999);
                        margin-right: 6px;

                    }

                    .value {
                        .sc(36px, @moneyColor);
                    }
                }

                .btn-pay-order {
                    background: @mainColor;
                    .sc(30px, white);
                    padding: 14px 48px;
                    border-radius: 34px;
                }
            }

        }
    }
</style>

<template>
    <div class="container">
        <header-top showBack>
            <section slot="right">
                <button class="header-btn" @click="isEdit = !isEdit">{{isEdit ?'完成': '管理'}}</button>
            </section>
        </header-top>

        <template v-if="cartListWithCheck.length">
            <section class="shop-cart-group-list">
                <ul class="shop-cart-group" v-for="product in cartListWithCheck">
                    <li v-for="cartItem in product.skulist" class="shop-cart-item">
                        <section class="item-radio-section" @click.stop="switchCartChecked(cartItem)">
                            <img :src="getRadioUrl(cartItem._checked)" alt="">
                        </section>

                        <section class="item-img-section" @click="goGoodsDetail(product)">
                            <img v-lazy="product.PRpic" alt="">
                        </section>

                        <section class="item-detail-section">
                            <p class="right-hd">
                                {{product.PRname}}
                            </p>
                            <p class="right-bd">
                            <span class="sku">
                                {{`${cartItem.colorname} ${cartItem.sizename}`}}
                            </span>
                                <span class="status">
                                {{statusToTxt(cartItem.SCstatus)}}
                            </span>
                            </p>
                            <section class="right-ft">
                                <span class="price">￥{{product.PRprice}}</span>
                                <count :key="cartItem.SCid" :count="cartItem.number"
                                       @minus="updateCartNumber(cartItem, cartItem.number-1)"
                                       @add="updateCartNumber(cartItem, cartItem.number+1)"
                                       @input="updateCartNumber(cartItem,$event)"
                                ></count>
                            </section>
                        </section>
                    </li>
                </ul>
            </section>
        </template>
        <place-holder v-else title="请返回商城选购商品后再来看看"></place-holder>


        <section class="pay-order-block">
            <section class="pay-order-left" @click="switchAllChecked">
                <img class="img-check-all" :src="getRadioUrl(checkedAll)" alt="">
                <span class="label-check-all">全选</span>
            </section>
            <section class="pay-order-right">
                <template v-if="isEdit">
                    <button class="btn-pay-order" @click="deleteCart">删 除</button>

                </template>
                <template v-else>

                    <p class="total-block">
                        <span class="label">合计</span>
                        <span class="value">￥{{totalCount}}</span>
                    </p>

                    <button class="btn-pay-order" @click="gotoPayOrder">结 算</button>
                </template>
            </section>
        </section>
    </div>
</template>

<script>
    import Count from "src/components/common/count";
    import PlaceHolder from "src/components/common/placeHolder";
    import {getShoppingCart, updateShoppingCartNumber, deleteShoppingCart, checkBail} from "src/api/api";

    export default {
        name: "shopCart",

        components: {
            Count,
            PlaceHolder
        },

        data() {
            return {
                cartList: [],
                scStatus: [
                    {
                        id: 1,
                        name: '可结算',    //  不显示
                    }, {
                        id: 2,
                        name: '库存不足'
                    }, {
                        id: 3,
                        name: '请重新选择商品规格'
                    }, {
                        id: 4,
                        name: '商品已下架'
                    },
                ],

                isEdit: false,
                checkedScIds: [],

                checkedAll: false,
            }
        },

        watch: {
            checkedScIds(val) {
                let hasNoChecked = false;
                for (let i = 0; i < this.cartList.length; i++) {
                    let currentProduct = this.cartList[i];

                    for (let j = 0; j < currentProduct.skulist.length; j++) {
                        let currentCartItem = currentProduct.skulist[j];

                        if (!this.checkedScIds.includes(currentCartItem.SCid)) {
                            hasNoChecked = true;
                            this.checkedAll = false
                            return
                        }
                    }
                }

                if (!hasNoChecked) {
                    this.checkedAll = true;
                }
            }
        },

        computed: {
            cartListWithCheck() {
                return this.cartList.map(product => {
                    product.skulist = product.skulist.map(cartItem => {
                        cartItem._checked = this.checkedScIds.includes(cartItem.SCid);
                        return cartItem;
                    });
                    return product;
                })
            },

            totalCount() {
                let count = 0

                if (this.isEdit) {
                    count = 0
                } else {
                    if (this.cartListWithCheck) {
                        for (let i = 0; i < this.cartListWithCheck.length; i++) {
                            let currentProduct = this.cartListWithCheck[i];

                            for (let j = 0; j < currentProduct.skulist.length; j++) {
                                let currentCartItem = currentProduct.skulist[j];

                                if (currentCartItem._checked) {
                                    count += currentCartItem.number * currentProduct.PRprice;
                                }
                            }
                        }
                    }
                }

                return count.toFixed(2);
            }
        },

        methods: {
            async gotoPayOrder() {
                let checkBailData = await checkBail();

                if (checkBailData.bailstatus == 1) {
                    // 判断选中的商品内的SCstatus
                    let checkedCartData = [];

                    if (!this.checkedScIds.length) {
                        this.$toast('您还没有选择要商品哦');
                        return
                    }

                    for (let i = 0; i < this.cartList.length; i++) {
                        let currentProduct = this.cartList[i];

                        checkedCartData.push({
                            PRid: currentProduct.PRid,
                            PRname: currentProduct.PRname,
                            PRpic: currentProduct.PRpic,
                            PRprice: currentProduct.PRprice,
                            PRlogisticsfee: currentProduct.PRlogisticsfee,
                            skulist: []
                        });

                        for (let j = 0; j < currentProduct.skulist.length; j++) {
                            let currentCartItem = currentProduct.skulist[j];

                            if (currentCartItem._checked) {
                                if (currentCartItem.SCstatus == 1) {
                                    checkedCartData[i].skulist.push(
                                        {
                                            psid: currentCartItem.PSid,
                                            colorname: currentCartItem.colorname,
                                            sizename: currentCartItem.sizename,
                                            number: currentCartItem.number,
                                        }
                                    )
                                } else {
                                    this.$toast(`请取消选择 ${currentProduct.PRname} ${currentCartItem.colorname} ${currentCartItem.sizename},原因: ${this.statusToTxt(currentCartItem.SCstatus)}`);
                                    return
                                }
                            }
                        }

                    }

                    this.$router.push({
                        path: '/payOrder',
                        query: {
                            cartList: JSON.stringify(checkedCartData)
                        }
                    })
                    console.log(checkedCartData);
                } else if (checkBailData.bailstatus == 2) {
                    this.$messagebox.confirm(`还需交纳保证金(${checkBailData.data.shouldpay}元)后才可下单,是否前往钱包页交纳?`).then(
                        () => {
                            this.$router.push('/wallet')
                        }
                    )
                } else if (checkBailData.bailstatus == 3) {
                    this.$toast('保证金退还中,无法下单!');

                }
            },

            setCartList() {
                getShoppingCart().then(
                    resData => {
                        if (resData) {
                            let data = resData.data;

                            this.cartList = data;
                        }
                    }
                )
            },
            statusToTxt(status) {
                if (status == 1) {
                    return ''
                } else {
                    return this.scStatus.find(item => item.id == status).name;
                }
            },
            goGoodsDetail(goods) {
                this.$router.push({
                    path: '/goodsDetail',
                    query: {
                        prid: goods.PRid
                    }
                });
            },

            getRadioUrl(checked) {
                return checked ? '/static/images/radio_check.png' : '/static/images/radio_uncheck.png';
            },
            switchCartChecked(cartItem) {
                let index = this.checkedScIds.indexOf(cartItem.SCid),
                    exist = index != -1;

                if (exist) {
                    this.checkedScIds.splice(index, 1)
                } else {
                    this.checkedScIds.push(cartItem.SCid);
                }
            },

            updateCartNumber(cartItem, newNumber) {
                if(newNumber == cartItem.number){
                    return
                }

                if (newNumber) {
                    updateShoppingCartNumber(cartItem.PSid, newNumber).then(
                        resData => {
                            this.setCartList();
                        }
                    )
                } else {
                    this.$messagebox.confirm('确认要从购物车删掉该商品?').then(
                        action => {
                            deleteShoppingCart([cartItem.SCid]).then(
                                resData => {
                                    if (resData) {
                                        let data = resData.data;
                                        let scIndex = this.checkedScIds.indexOf(cartItem.SCid);

                                        if (scIndex != -1) {
                                            this.checkedScIds.splice(scIndex, 1);
                                        }

                                        this.setCartList();
                                        this.$toast('删除成功');
                                    }
                                }
                            )
                        }
                    )
                }
            },

            switchAllChecked() {
                if (this.checkedAll) {
                    this.checkedScIds = [];
                    this.checkedAll = false;
                } else {
                    let allScIds = [];

                    for (let i = 0; i < this.cartList.length; i++) {
                        let currentProduct = this.cartList[i];

                        for (let j = 0; j < currentProduct.skulist.length; j++) {
                            let currentCartItem = currentProduct.skulist[j];

                            allScIds.push(currentCartItem.SCid);
                        }
                    }

                    if (allScIds.length) {
                        this.checkedScIds = allScIds;
                        this.checkedAll = true;
                    }
                }
            },

            deleteCart() {
                if (this.checkedScIds.length) {
                    deleteShoppingCart(this.checkedScIds).then(
                        resData => {
                            if (resData) {
                                let data = resData.data;

                                this.checkedScIds = [];
                                this.setCartList();
                                this.$toast('删除成功');
                            }
                        }
                    )
                } else {
                    this.$toast('您还没有选择要商品哦')
                }
            },
        },

        created() {
            this.setCartList();

        },
    }
</script>

