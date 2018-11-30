<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();
        padding-bottom: 150px;
        .bgw();

        .banner {
            height: 750px;
            .bs(10px, 3px, 6px);

            .banner-img {
                .wl(100%, 100%);
                /*max-width: 100%;*/
                /*max-height: 100%;*/
            }
        }

        .goods-detail {
            padding: 30px;
            .bs(10px, 3px, 6px);

            .detail-row-one {
                .fj();
                margin-bottom: 20px;

                .name {
                    .sc(32px, #666666);
                    font-weight: bold;
                }
                .price {
                    .sc(32px, @moneyColor);
                }
            }
            .detail-row-two {
                .fj();
                color: #999999;
            }
        }

        .choose-sku {
            padding: 30px;
            .bs(10px, 3px, 6px);
            .bgw();
            .fj();
            align-items: center;
            .fz(28px);

            .choose-sku-hd {
                .label {
                    color: #999999;
                    margin-right: 30px;
                }
                .type {
                    color: #666666;

                }
            }
            .choose-sku-ft {
                .wl(10px, 17px);
            }
        }

        .choose-goods-spec {
            width: 100%;
            padding: 30px;
            box-sizing: border-box;

            .close-row {
                .fj(flex-end);
                padding-top: 22px;
                padding-right: 22px;
                margin-bottom: 30px;

                img {
                    .wl(35px, 35px);
                }
            }

            .goods-spec-list {
                .goods-spec-item {
                    margin-bottom: 22px;

                    .title {
                        color: @999;
                        margin-bottom: 17px;
                    }

                    .spec-list {
                        .fj(flex-start);
                        flex-wrap: wrap;

                        .spec-item {
                            padding: 5px 50px;
                            margin-right: 30px;
                            border-radius: 30px;
                            border: 2px solid @mainColor;
                            margin-bottom: 20px;

                            &.disabled {
                                background: @999;
                            }
                            &.active {
                                color: white;
                                background: @mainColor;
                            }
                        }

                    }

                }
            }
        }

        .num-block {
            .fj();
            align-items: center;
            margin-top: 30px;

            .stock {
                .sc(28px, @666);
            }
        }
    }
</style>

<template>
    <div class="container">
        <header-top :showBack="true">
            <section slot="right">
                <router-link tag="button" to="/shopCart" class="header-btn">购物车</router-link>
            </section>
        </header-top>

        <mt-swipe class="banner" :stopPropagation="true">
            <mt-swipe-item v-for="item in product.sowingmap" :key="item">
                <img class="banner-img" :src="item" alt="">
            </mt-swipe-item>
        </mt-swipe>

        <section class="goods-detail">
            <p class="detail-row-one">
                <span class="name">{{product.PRname}}</span>
                <span class="price">￥{{product.PRprice}}</span>
            </p>
            <p class="detail-row-two">
                <span>{{product.PRlogisticsfee ? `快递(单件):${product.PRlogisticsfee}元`:'包邮'}}</span>
                <span style="text-decoration: line-through;">￥{{product.PRoldprice}}</span>
            </p>
        </section>

        <!--<section class="choose-sku" @click="showChooseSpec">-->
            <!--<span class="choose-sku-hd">-->
              <!--<span class="label">选择</span>-->
              <!--<span class="type">类型 尺寸</span>-->
            <!--</span>-->
            <!--<img src="/static/images/arrow.png" alt="" class="choose-sku-ft">-->
        <!--</section>-->

        <section class="choose-goods-spec">
            <!--<section class="close-row">-->
                <!--<img src="/static/images/close.png" alt="" @click="chooseSpecVisible=false">-->
            <!--</section>-->

            <section class="goods-spec-list">
                <section class="goods-spec-item">
                    <p class="title">
                        颜色
                    </p>

                    <ul class="spec-list">
                        <li v-for="color in colorList" :class="{'spec-item': true, 'active': color.id == choosedColor}"
                            @click="chooseColor(color)">
                            {{color.name}}
                        </li>
                    </ul>
                </section>
                <section class="goods-spec-item">
                    <p class="title">
                        尺码
                    </p>

                    <ul class="spec-list">
                        <li v-for="size in sizeList" :class="{'spec-item': true, 'active': size.id == choosedSize}"
                            @click="chooseSize(size)">
                            {{size.name}}
                        </li>
                    </ul>
                </section>
            </section>

            <section class="num-block">
                <span class="stock">库存:{{allStock || (choosedSku? choosedSku.PSstock: 0)}}件</span>
                <count :count="count" @add="changeCount( count + 1)" @minus="changeCount( count -1)"
                       @input="changeCount"></count>
            </section>

            <section class="my-confirm-btn-wrap" style="margin-top: 50px;margin-bottom: 40px;">
                <button v-show="addToCartEnable" class="my-confirm-btn add-shop-cart" @click="addToCart">加 入 购 物 车
                </button>
                <button v-show="!addToCartEnable" class="my-confirm-btn disabled add-shop-cart ">加 入 购 物 车</button>
            </section>
        </section>
    </div>
</template>

<script>
    import Count from "src/components/common/count";
    import {title, getProductDetails, addShoppingCart} from "src/api/api";


    export default {
        name: "goodsDetail",

        components: {
            Count
        },

        data() {
            return {
                product: {},
                colorList: [],
                sizeList: [],
                choosedColor: '',
                choosedSize: '',

                chooseSpecVisible: false,
                count: 1,
            }
        },

        computed: {
            allStock() {
                if (!(this.choosedSku) && this.product.skulist) {
                    let count = 0;

                    for (let i = 0; i < this.product.skulist.length; i++) {
                        count += this.product.skulist[i].PSstock;
                    }

                    return count;
                }
            },
            choosedSku() {
                if (this.choosedColor && this.choosedSize) {
                    let correspondingSku = this.product.skulist.find(
                        item => {
                            return item.colorid == this.choosedColor && item.sizeid == this.choosedSize;
                        }
                    );

                    return correspondingSku;
                } else {
                    return null
                }
            },

            addToCartEnable() {
                if (this.choosedSku) {
                    return this.count <= this.choosedSku.PSstock;
                } else {
                    return true
                }
            },
        },

        methods: {
            showChooseSpec() {
                this.chooseSpecVisible = true;

                if (this.product.skulist.length == 1) {
                    this.choosedColor = this.product.skulist[0].colorid;
                    this.choosedSize = this.product.skulist[0].sizeid;
                }
            },
            chooseColor(color) {
                if (this.choosedColor == color.id) {
                    this.choosedColor = '';
                } else {
                    this.choosedColor = color.id;
                }
            },
            chooseSize(size) {
                if (this.choosedSize == size.id) {
                    this.choosedSize = '';
                } else {
                    this.choosedSize = size.id;
                }
            },

            changeCount(newCount) {
                this.count = Number( newCount);
            },

            addToCart() {
                if (this.choosedSku) {
                    if(this.count){
                        addShoppingCart(this.product.PRid, this.choosedSku, this.count).then(
                            resData => {
                                if (resData) {
                                    let data = resData.data;

                                    this.count = 1;
                                    // this.chooseSpecVisible = false;
                                    this.$toast('已添加到购物车')
                                }
                            }
                        )
                    }else{
                        this.$toast('请确保数量大于1!');
                    }
                } else {
                    this.$toast('请选择颜色和尺码!');
                }
            }
        },

        created() {
            getProductDetails(this.$route.query.prid).then(
                resData => {
                    if (resData) {
                        let data = resData.data;

                        this.product = data;

                        for (let i = 0; i < data.skulist.length; i++) {
                            if (!this.colorList.find(item => item.id == data.skulist[i].colorid)) {
                                this.colorList.push({
                                    id: data.skulist[i].colorid,
                                    name: data.skulist[i].colorname,
                                });
                            }

                            if (!this.sizeList.find(item => item.id == data.skulist[i].sizeid)) {
                                this.sizeList.push({
                                    id: data.skulist[i].sizeid,
                                    name: data.skulist[i].sizename,
                                });
                            }
                        }

                        if (this.product.skulist.length == 1) {
                            this.choosedColor = this.product.skulist[0].colorid;
                            this.choosedSize = this.product.skulist[0].sizeid;
                        }
                    }
                }
            )
        },
    }
</script>

