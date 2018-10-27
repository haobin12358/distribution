<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        min-height: 100vh;
        .nav-bar {
            .fj();
            background: white;
            margin-bottom: 10px;

            .nav-bar-item {
                flex: 1;
                height: 80px;
                .fontc(80px);
                text-align: center;

                &.active {
                    color: @mainColor;
                    border-bottom: 3px solid @mainColor;
                }
            }

        }

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

                .goods-list{
                    border-bottom: 1px solid @grayBorderColor;
                    margin-bottom: 10px;

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

        <ul class="nav-bar" >
            <li v-for="item in orderType" :class="{'nav-bar-item': true, 'active': item.value == selectOrderType}"
            @click="switchOrderType(item)">{{item.label}}</li>
        </ul>

        <ul class="order-list">
            <li v-for="item in orderListCmp" class="order-item">
                <header class="order-item-header">
                    <p class="row-one">
                        <span class="no">编号：{{item.OIsn}}</span>
                        <span class="status">{{item.OIstatusZh}}</span>
                    </p>
                    <p class="row-two">
                        时间：{{item.OIcreatetime}}
                    </p>
                </header>

                <ul class="goods-list">
                    <li class="goods-item" v-for="product in item.product_list">
                        <section class="goods-img">
                            <img src="/static/images/testbg.jpg" alt="">
                        </section>
                        <section class="goods-description">
                            <p class="row-one">
                                <span class="goods-name">{{product.PRname}}</span>
                                <span class="goods-price">￥{{product.PRprice}}</span>
                            </p>
                            <p class="row-two">
                                ×3
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
    </div>
</template>

<script>
    import {getOrderList} from "src/api/api"
    import LoadMore from "src/components/common/loadMore"


    export default {
        name: "order",

        data() {
            return {
                selectOrderType: 0,
                orderType: [
                    {
                        label: '全部',
                        value: 0,
                    },{
                        label: '待发货',
                        value: 1,
                    },{
                        label: '已发货',
                        value: 2,
                    },{
                        label: '已完成',
                        value: 3,
                    },
                ],

                orderList: [],
            }
        },

        computed:{
            //  翻译状态
            orderListCmp(){
                let rst = this.orderList.map(item => {
                    item.OIstatusZh = this.orderType.find(type => type.value == item.OIstatus).label;
                    return item;
                })

                return rst;
            },
        },

        components: {
            LoadMore
        },

        methods: {
            //  切换订单类型
            switchOrderType(item){
                if(this.selectOrderType != item.value){
                    this.selectOrderType = item.value;
                    getOrderList(this.selectOrderType).then(
                        ({data}) => {
                            this.orderList = data;
                        }
                    )

                }
            },
            getOrderList(replace){

            },
        },

        created(){
            getOrderList(this.selectOrderType).then(
                ({data}) => {
                    this.orderList = data;
                }
            )
        },

    }
</script>

