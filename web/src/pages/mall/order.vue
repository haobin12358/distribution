<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        min-height: 100vh;

        .order-list {

            .order-item {
                padding: 16px 26px;
                margin-bottom: 10px;
                background: white;

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

                .goods-list {
                    border-bottom: 1px solid @grayBorderColor;
                    margin-bottom: 10px;

                    .goods-item {
                        padding: 36px 0;
                        .fj();

                        .goods-img {
                            .wl(100px, 100px);
                            margin-right: 40px;

                            img {
                                .wl(100%, 100%);
                            }
                        }

                        .goods-description {
                            .fj();
                            flex-direction: column;
                            flex: 1;

                            .row-one {
                                .fj();

                                .goods-name {

                                }
                                .goods-price {
                                    color: @lightFontColor;
                                }
                            }

                            .row-two {
                                color: @lightFontColor;
                                text-align: right;
                            }
                        }

                    }
                }

                .order-item-total {
                    .fj(flex-end);
                    padding-top: 10px;

                    .total-num {
                        margin-right: 10px;
                    }
                    .total-price {

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
            <li v-for="item in orderType" :class="{'nav-bar-item': true, 'active': item.value == selectOrderType}"
                @click="switchOrderType(item)">
                {{item.label}}({{item.num}})
            </li>
        </ul>

        <template v-if="orderList.length">
            <ul class="order-list">
                <li v-for="item in orderList" @click="gotoOrderDetail(item.OIsn)" class="order-item">
                    <header class="order-item-header">
                        <p class="row-one">
                            <span class="no">编号：{{item.OIsn}}</span>
                            <span class="status">{{statusZh(item.OIstatus)}}</span>
                        </p>
                        <p class="row-two">
                            时间：{{item.OIcreatetime}}
                        </p>
                    </header>

                    <ul class="goods-list">
                        <li class="goods-item" v-for="product in item.product_list">
                            <section class="goods-img">
                                <img :src="product.PRimage" alt="">
                            </section>
                            <section class="goods-description">
                                <p class="row-one">
                                    <span class="goods-name">{{product.PRname}}</span>
                                    <span class="goods-price">￥{{product.PRprice}}</span>
                                </p>
                                <p class="row-two">
                                    ×{{product.PRnum}}
                                </p>
                            </section>
                        </li>
                    </ul>
                    <footer class="order-item-total">
                        <span class="total-num">共{{item.product_list.length}}件商品</span>
                        <span class="total-price">价值:￥{{item.OImount}}</span>
                    </footer>
                </li>
            </ul>
            <load-more :type="loadingType"></load-more>
        </template>
        <place-holder v-else title="没有该类订单"></place-holder>

    </div>
</template>

<script>
    import {getOrderList} from "src/api/api"
    import LoadMore from "src/components/common/loadMore"
    import common from "src/common/js/common"
    import PlaceHolder from "src/components/common/placeHolder"


    export default {
        name: "order",

        data() {
            return {
                selectOrderType: 0,
                orderType: [
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
                ],

                page: 1,    // 页数
                count: 10,  // 条数
                loadingType: 'normal',  // 加载组件加载状态
                orderList: [],
            }
        },

        computed: {},

        components: {
            LoadMore,
            PlaceHolder
        },

        methods: {
            gotoOrderDetail(OIsn){
                this.$router.push({
                    path: '/mallOrderDetail',
                    query: {
                        OIsn
                    }
                })
            },
            //  切换订单类型
            switchOrderType(item) {
                if (this.selectOrderType != item.value) {
                    this.selectOrderType = item.value;
                    this.setOrderList(true);
                }
            },
            //  订单状态翻译
            statusZh(status) {
                return this.orderType.find(item => item.value == status).label;
            },
            // 滚动条监听事件
            touchMove() {
                let scrollTop = common.getScrollTop();
                let scrollHeight = common.getScrollHeight();
                let ClientHeight = common.getClientHeight();

                if (scrollTop + ClientHeight >= scrollHeight - 10 && this.loadingType == 'normal') {
                    console.log('滚动');
                    this.setOrderList();
                }
            },
            setOrderList(replace) {
                if (replace) {
                    this.page = 1;
                }
                this.loadingType = 'loading';

                getOrderList(this.selectOrderType, this.page, this.count).then(
                    (resData) => {
                        if(resData){
                            let data = resData.data;

                            if(this.selectOrderType == 0){
                                this.orderType[0].num = resData.state0_num;
                                this.orderType[1].num = resData.state1_num;
                                this.orderType[2].num = resData.state2_num;
                                this.orderType[3].num = resData.state3_num;
                            }

                            if (data.length < this.count) {
                                this.loadingType = 'nomore';
                            } else {
                                this.loadingType = 'normal';
                            }

                            if (replace) {
                                this.orderList = data;
                            } else {
                                this.orderList = this.orderList.concat(data);
                            }

                            this.page++;
                        }
                    }
                )
            },
        },

        destroyed() {
            window.removeEventListener('scroll', this.touchMove);

        },

        async mounted() {
            await this.setOrderList(true);
            window.addEventListener('scroll', this.touchMove);
        },

    }
</script>

