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
                    span {
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
                <span class="detail-item-value">{{details.OIstatusZh}}</span>
            </li>
            <li class="detail-item">
                <span class="detail-item-label">商品件数：</span>
                <span class="detail-item-value"> {{details.pdCount}}件</span>
            </li>
            <li class="detail-item">
                <span class="detail-item-label">邮费：</span>
                <span class="detail-item-value">￥{{details.OIlogisticsfee}}</span>
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
                <template v-for="product in details.product_list">

                <li class="product-item" v-for="cartItem in product.skulist">
                    <img v-lazy="product.PRimage" alt="" class="product-img">

                    <span class="name">{{product.PRname}}</span>

                    <p class="num">
                        <span class="price">￥{{product.PRprice}}</span>
                        <span class="shop-num">x{{cartItem.number}}</span>
                    </p>
                </li>
                </template>
            </ul>

            <template v-if="details.expressnum">
                <li class="detail-item">
                    <span class="detail-item-label">快递单号：</span>
                </li>

                <section class="details-delivery" @click="gotoKuaidi100">
                    <span class="delivery-company">
                        {{details.expressname}}
                    </span>
                    <section class="delivery-no">
                        <span>{{details.expressnum}}</span>
                        <img class="arrow" src="/static/images/arrow.png" alt=""/>
                    </section>
                </section>
            </template>
        </ul>
    </div>
</template>

<script>
    import {getOrderDetails} from "src/api/api"

    let orderType = [
        {
            label: '全部',
            value: 0,
            num: 0
        }, {
            label: '待发货',
            value: 1,
            num: 0

        }, {
            label: '已发货',
            value: 2,
            num: 0
        }, {
            label: '已完成',
            value: 3,
            num: 0
        },
    ];

    export default {
        name: "orderDetail",

        data() {
            return {
                details: {}
            }
        },

        components: {},

        computed: {

        },

        methods: {
            //  订单状态翻译
            statusZh(status) {
                let res= '';

                switch (status) {
                    case 1:
                        res = '待发货';
                        break;
                    case 2:
                        res = '已发货'
                        break
                    case 3:
                        res = '已完成'
                        break;
                    case 4:
                        res = '分拣中'
                        break
                    case 5:
                        res = '已取消'
                        break
                }

                return res;
            },

            setDetail(OIsn) {
                getOrderDetails(OIsn).then(
                    ({data}) => {
                        this.details = data;
                        this.details.OIstatusZh = this.statusZh(this.details.OIstatus);
                        let count = 0;
                        for (let i = 0; i < this.details.product_list.length; i++) {
                            count +=  this.details.product_list[i].PRnum;
                        }
                        this.details.pdCount = count;
                    }
                )
            },
            gotoKuaidi100() {
                location.href = `https://m.kuaidi100.com/index_all.html?postid=${this.details.expressnum}#result`;
            },
        },

        created() {
            this.setDetail(this.$route.query.OIsn);
        },
    }
</script>

