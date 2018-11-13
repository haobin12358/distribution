<style lang="less" scoped>
    @import "../../common/css/index";

    .container {

        .section-one {
            .fj();
            margin-bottom: 33px;

            .section-one-block {
                flex: 1;
                .bs(0, .03rem, .1rem);
                .wl(2.7rem, auto);
                padding: .15rem .15rem .5rem;

                .head-title {
                    .fz(.2rem);
                    padding-left: .4rem;
                    padding-bottom: .2rem;
                    .bdb();
                }

                &.schedule {
                    margin-right: .4rem;

                    .action-wrap {
                        padding-top: .1rem;
                        .action-btn {
                            padding: .2rem .2rem;
                            color: white;
                            .fz(.23rem);
                            border-radius: .1rem;
                            margin-right: .1rem;
                            margin-top: .1rem;

                            &.withdraw {
                                background: #EDB3B1;
                            }
                            &.charge {
                                background: #9FD0BF;

                            }
                            &.margin {
                                background: #91AEB5;

                            }

                        }
                    }
                }

                &.trade-data {
                    .trade-list {
                        .fj();
                        flex-wrap: wrap;
                        padding: 0;

                        .trade-item {
                            .wl(50%, auto);
                            padding: .2rem;
                            box-sizing: border-box;

                            &:nth-child(1) {
                                border-right: 1px solid #999999;
                                /*border-left: none;*/
                            }
                            &:nth-child(2) {
                                /*border-top: 1px solid #999999;*/
                                /*border-bottom: 1px solid #999999;*/
                            }

                            .today-data {
                                .fj(flex-start);
                                margin-bottom: .2rem;

                                img {
                                    .wl(.67rem, .67rem);
                                    margin-right: .2rem;
                                }

                                .detail {
                                    .fjc();

                                    .num {
                                        color: #d80000;

                                    }

                                }
                            }
                            .yesterday-data {
                                .sc(.2rem, gray);
                                .fj();

                            }

                        }
                    }
                }
            }
        }

        .section-two {
            margin-bottom: .2rem;
            .head-title {
                .fz(.2rem);
                padding-left: .4rem;
                padding-bottom: .2rem;
            }

            .chart {
                .bs(0, .03rem, .1rem);
                .wl(100%, 5rem)
            }
        }
    }
</style>

<template>
    <div class="container">
        <el-breadcrumb style="margin-bottom: .2rem;" separator="/">
            <el-breadcrumb-item>概览首页</el-breadcrumb-item>
        </el-breadcrumb>

        <section class="section-one">
            <section class="section-one-block schedule">
                <header class="head-title fcm">
                    代办事项
                </header>

                <section class="action-wrap">
                    <router-link tag="button" to="/service/withdraw" class="action-btn withdraw">
                        提现申请 {{withdrawNum}}
                    </router-link>
                    <router-link tag="button" to="/service/charge" class="action-btn charge">
                        余额充值 {{chargeNum}}
                    </router-link>
                    <router-link tag="button" to="/service/register" class="action-btn margin">
                        新代理注册 {{registerNum}}
                    </router-link>
                    <router-link tag="button" to="/order/index" class="action-btn margin">
                        待发货 {{waitDeliverNum}}
                    </router-link>

                </section>
            </section>

            <section class="section-one-block trade-data">
                <header class="head-title fcm">
                    交易数据
                </header>

                <ul class="trade-list">
                    <li class="trade-item">
                        <section class="today-data">
                            <img src="/static/images/sale_money.png" alt="">

                            <section class="detail">
                                <span>今日交易额</span>
                                <span class="num today-sale">￥ {{todaySaleMoney}}</span>
                            </section>
                        </section>

                        <section class="yesterday-data">
                            <span class="label">今日交易额</span>
                            <span class="value">￥ {{yesterdaySaleMoney}}</span>
                        </section>

                    </li>

                    <li class="trade-item">
                        <section class="today-data">
                            <img src="/static/images/order.png" alt="">

                            <section class="detail">
                                <span>今日订单数</span>
                                <span>{{todaySaleMoney}}</span>
                            </section>
                        </section>

                        <section class="yesterday-data">
                            <span class="label">昨日订单数</span>
                            <span class="value">{{yesterdaySaleMoney}}</span>
                        </section>

                    </li>


                </ul>
            </section>
        </section>

        <section class="section-two">
            <section class="chart" id="sale-chart"></section>
        </section>

        <section class="section-two">
            <section class="chart" id="order-chart"></section>
        </section>


    </div>
</template>

<script>
    export default {
        name: "index",

        data() {
            return {
                waitDeliverNum: 0,  //  待发货
                chargeNum: 0,       //  充值
                registerNum: 0,  //  保证金
                withdrawNum: 0,     //  提现

                todaySaleMoney: 0,
                yesterdaySaleMoney: 0,

                todayOrderNum: 0,
                yesterdayOrderNum: 0,

                msg: 'Welcome to Your Vue.js App',
                chartData: [],
            }
        },

        components: {},

        computed: {},

        methods: {
            //  左上角快捷方式数字
            setShortCutData() {
                this.$http.post(this.$api.getAllOrder,
                    {
                        "page_size": 1,
                        "page_num": 1,
                        "oisn": '',
                        "starttime": '',
                        "endtime": '',
                        "status": 1,
                        "username": '',
                        "userphonenum": '',
                        "productname": '',
                    }, {
                        noLoading: true,
                        params: {
                            token: this.$common.getStore('token')
                        }
                    }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.waitDeliverNum = resData.mount || 0;
                        }
                    }
                );

                this.$http.post(this.$api.getRegisterRecord, {
                    "status": 1,

                    "page_size": 1,
                    "page_num": 1,
                }, {
                    noLoading: true,
                    params: {
                        token: this.$common.getStore('token')
                    }
                }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.registerNum = resData.mount || 0;
                        }
                    }
                );

                this.$http.post(this.$api.getAllChargemoney,
                    {
                        status: 1,
                        "page_size": 1,
                        "page_num": 1,
                    }, {
                        noLoading: true,
                        params: {
                            token: this.$common.getStore('token')

                        }
                    }).then(
                    res => {

                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.chargeNum = resData.mount || 0;
                        }
                    }
                )

                this.$http.post(this.$api.getAlluserDrawmoneyList,
                    {
                        status: 1,

                        "page_size": 1,
                        "page_num": 1,
                    }, {
                        noLoading: true,
                        params: {
                            token: this.$common.getStore('token')

                        }
                    }).then(
                    res => {

                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.withdrawNum = resData.mount || 0;
                        }
                    }
                )

            },

            setSevenDaysData() {
                this.$http.get(this.$api.getSevenDaysData,
                    {
                        params: {
                            token: this.$common.getStore('token')

                        }
                    }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.todaySaleMoney = data[0].money;
                            this.yesterdaySaleMoney = data[1].money;
                            this.todayOrderNum = data[0].count;
                            this.yesterdayOrderNum = data[1].count;

                            let revData = data.reverse();
                            this.drawLine(revData)
                        }
                    }
                )
            },

            drawLine(chartData) {
                // 基于准备好的dom，初始化echarts实例
                let myChart = this.$echarts.init(document.getElementById('order-chart'));

                let orderAxis,
                    orderSeries;

                orderAxis = chartData.map(item => item.date);
                orderSeries = chartData.map(item => item.count);


                // 绘制图表
                myChart.setOption({
                    title: {text: '近7天的订单量'},
                    tooltip: {
                        trigger: 'axis',

                    },
                    xAxis: {
                        type: 'category',
                        data: orderAxis
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [{
                        data: orderSeries,
                        type: 'line'
                    }]
                });


                let myChart2 = this.$echarts.init(document.getElementById('sale-chart'));

                let saleAxis = chartData.map(item => item.date);
                let saleSeries = chartData.map(item => item.money);
                // 绘制图表
                myChart2.setOption({
                    title: {text: '近7天的销售额'},
                    tooltip: {
                        trigger: 'axis',

                    },
                    xAxis: {
                        type: 'category',
                        data: saleAxis
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [{
                        data: saleSeries,
                        type: 'line'
                    }]
                });
            }
        },

        mounted() {
            this.setShortCutData();
            this.setSevenDaysData();

            this.drawLine();
        },
    }
</script>

