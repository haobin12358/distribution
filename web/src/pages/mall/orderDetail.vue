<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        background: white;
        padding-bottom: 200px;

        .detail-list {
            padding: 20px 27px 0;

            .detail-item {
                .fj();
                margin-bottom: 20px;

                .detail-item-label {
                    color: #999999;

                }
                .detail-item-value {
                    color: black;

                }
            }

            .product-list {
                .product-item {
                    .fj();
                    align-items: center;
                    margin-bottom: 15px;

                    .product-img {
                        .wl(100px, 100px);
                        margin-right: 30px;
                    }

                    .name {
                        flex: 1;
                        .sc(28px, #333333);
                    }

                    .num {
                        .fj();
                        flex-direction: column;
                        align-items: flex-end;

                        .price {
                        }
                        .shop-num {
                        }
                    }
                }
            }

            .details-delivery {
                .fj();
                align-items: center;

                .delivery-company {
                    flex: 1;
                }

                .delivery-no {
                    // .fj();
                    // align-items: center;
                    span    {
                        line-height: 26px;
                    }

                    .arrow {
                        margin-left: 20px;
                        .wl(15px, 26px);
                    }
                }
            }
        }
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <ul class="detail-list">
            <li class="detail-item">
                <span class="detail-item-label">订单编号：</span>
                <span class="detail-item-value">{{details.OIsn}}</span>
            </li>
            <li class="detail-item">
                <span class="detail-item-label">下单时间：</span>
                <span class="detail-item-value">{{details.createtime}}</span>
            </li>
            <li class="detail-item">
                <span class="detail-item-label">状态：</span>
                <span class="detail-item-value">{{details.OIstatus}}</span>
            </li>
            <li class="detail-item">
                <span class="detail-item-label">商品件数：</span>
                <span class="detail-item-value">{{details.OIcreatetime}} 件</span>
            </li>
            <li class="detail-item">
                <span class="detail-item-label">订单金额：</span>
                <span class="detail-item-value">￥{{details.OImount}}</span>
            </li>
            <li class="detail-item">
                <span class="detail-item-label">收件人：</span>
                <span class="detail-item-value">{{details.username}}</span>
            </li>
            <li class="detail-item">
                <span class="detail-item-label">省份：</span>
                <span class="detail-item-value">{{details.provincename}}</span>
            </li>
            <li class="detail-item">
                <span class="detail-item-label">城市：</span>
                <span class="detail-item-value">{{details.cityname}}{{details.areaname || ''}}</span>
            </li>
            <li class="detail-item">
                <span class="detail-item-label">详细地址：</span>
                <span class="detail-item-value">{{details.details}}</span>
            </li>
            <li class="detail-item">
                <span class="detail-item-label">订单明细：</span>
            </li>

            <ul class="product-list">
                <li class="product-item" v-for="product in details.product_list">
                    <img :src="product.PRimage" alt="" class="product-img">

                    <span class="name">{{product.PRname}}</span>

                    <p class="num">
                        <span class="price">￥{{product.PRprice}}</span>
                        <span class="shop-num">x{{product.PRnum}}</span>
                    </p>
                </li>
            </ul>

            <li class="detail-item">
                <span class="detail-item-label">快递单号：</span>
            </li>

            <section class="details-delivery">
                <span class="delivery-company">
                    百世汇通
                </span>
                <span class="delivery-no">
                   <span>3381965843958</span>
                    <img class="arrow" src="/static/images/arrow.png" alt="">
                </span>
            </section>

        </ul>
    </div>
</template>

<script>
    import {getOrderDetails} from "src/api/api"

    export default {
        name: "orderDetail",

        data() {
            return {
                details: {}
            }
        },

        components: {},

        computed: {},

        methods: {
            setDetail(OIsn) {
                getOrderDetails(OIsn).then(
                    ({data}) => {
                        this.details = data;
                    }
                )
            }
        },

        created() {
            this.setDetail(this.$route.query.OIsn);
        },
    }
</script>

