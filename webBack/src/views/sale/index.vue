<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .sale-data-list {
            .fj();

            .sale-data-item {
                .wl(2.5rem, 2rem);
                padding: .3rem 0 .4rem;
                box-sizing: border-box;
                .fjc();
                align-items: center;
                border: 2px solid #46a0fc;

                &.active {
                    border-top: .1rem solid #46a0fc;

                }

                .num {
                    .sc(.5rem, #46a0fc);

                }

                .title {
                    text-align: center;

                }

            }
        }

        .chart {
            .bs(0, .03rem, .1rem);
            .wl(100%, 5rem);
            margin-bottom: .2rem;

        }
    }
</style>

<template>
    <div class="container">
        <h1 class="my-title">
            销售数据
        </h1>
        <ul class="sale-data-list">
            <li class="sale-data-item">
                <span class="num">{{countData.total_sale_num }}</span>
                <span class="title">总销售量（件）</span>

            </li>
            <li class="sale-data-item ">
                <span class="num">￥{{countData.total_sale_money | fixed2}}</span>
                <span class="title">总销售额（元）</span>

            </li>
            <li class="sale-data-item ">
                <span class="num">{{countData.total_order_num}}</span>
                <span class="title">订单数（笔）</span>

            </li>
            <li class="sale-data-item ">
                <span class="num">{{countData.total_agent_num}}</span>
                <span class="title">总代理数（人）</span>

            </li>

            <li class="sale-data-item ">
                <span class="num">￥{{countData.unit_price | fixed2}}</span>
                <span class="title">客单价（元）</span>

            </li>
            <li class="sale-data-item ">
                <span class="num">{{agentNum}}</span>
                <span class="title">该月新增代理数（人）</span>

            </li>
        </ul>

        <section class="chart" id="money-chart"></section>
        <section class="chart" id="order-chart"></section>
        <section class="chart" id="agent-chart"></section>
    </div>
</template>

<script>

    export default {
        name: "index",

        data() {
            return {
                countData: {},

                agentNum: 0,
                agentNumArr: [],
                agentChart: {},

                interval: null,
            }
        },

        components: {},

        computed: {},

        filters: {
            fixed2: function (value) {
                if(value){
                    return value.toFixed(2);
                }
            }
        },

        methods: {
            setCountData() {
                this.$http.get(this.$api.getCountData, {
                    params: {
                        token: this.$common.getStore('token')

                    }
                }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.countData = data;
                        }
                    }
                )
            },

            getThisYearDate() {
                this.$http.get(this.$api.getThisYearDate, {
                    params: {
                        token: this.$common.getStore('token')

                    }
                }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.date;

                            let revData = data.reverse();

                            this.drawLine(revData)
                        }
                    }
                )
            },

            drawLine(chartData) {
                let myChart = this.$echarts.init(document.getElementById('order-chart'));

                let orderAxis,
                    orderSeries;

                orderAxis = chartData.map(item => item.date);
                orderSeries = chartData.map(item => item.count);


                // 绘制图表
                myChart.setOption({
                    title: {text: '今年的订单量'},
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


                let myChart2 = this.$echarts.init(document.getElementById('money-chart'));

                let saleAxis = chartData.map(item => item.date);
                let saleSeries = chartData.map(item => item.money);
                // 绘制图表
                myChart2.setOption({
                    title: {text: '今年的销售额'},
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
            },

            drawAgentLine() {
                this.agentChart = this.$echarts.init(document.getElementById('agent-chart'));

                this.agentChart.setOption({
                    title: {
                        text: '当月实时新增代理数'
                    },
                    tooltip: {
                        trigger: 'axis',
                        formatter: function (params) {
                            params = params[0];
                            var date = new Date(params.name);
                            return date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear() + ' : ' + params.value[1];
                        },
                        axisPointer: {
                            animation: false
                        }
                    },
                    xAxis: {
                        type: 'time',
                        splitLine: {
                            show: false
                        }
                    },
                    yAxis: {
                        type: 'value',
                        boundaryGap: [0, '100%'],
                        splitLine: {
                            show: false
                        }
                    },
                    series: [{
                        name: '模拟数据',
                        type: 'line',
                        smooth: true,
                        showSymbol: false,
                        hoverAnimation: false,
                        data: this.agentNumArr
                    }]
                });
            },

            getThisMonthAgentnum() {
                this.$http.get(this.$api.getThisMonthAgentnum, {
                    noLoading: true,
                    params: {
                        token: this.$common.getStore('token')

                    }
                }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.agentNum = data.num;

                            // if(!this.agentNum.length){
                            //     for (let i = 0; i < 5; i++) {
                            //         this.agentNumArr.push({
                            //             name: i,
                            //             value: [
                            //                 Date.now(),
                            //                 data.num
                            //             ]
                            //         });
                            //     }
                            // }

                            this.agentNumArr.push({
                                name: Date.now(),
                                value: [
                                    Date.now(),
                                    data.num
                                ]
                            });

                            if (this.agentNum.length > 15) {
                                this.agentNumArr.shift();
                            }

                            this.agentChart.setOption({
                                series: [{
                                    data: this.agentNumArr
                                }]
                            });
                        }
                    }
                )
            }
        },

        destroyed() {
            if (this.interval) {
                clearInterval(this.interval)
            }
        },
        mounted() {
            this.setCountData();

            this.getThisYearDate();

            this.drawAgentLine();
            this.interval = setInterval(
                () => {
                    this.getThisMonthAgentnum();
                }, 5000
            )

        },
    }
</script>

