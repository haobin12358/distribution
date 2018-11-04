<style lang="less" scoped>
    @import "../../common/css/index";

    .container {

        .section-one {
            .fj();
            margin-bottom: 33px;

            .section-one-block {
                flex: 1;
                .bs(0, .03rem, .1rem);
                .wl(2.7rem, 4.4rem);
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
                        padding-top: .2rem;
                        .action-btn {
                            padding: .3rem .2rem;
                            color: white;
                            .fz(.23rem);
                            border-radius: .1rem;
                            margin-right: .1rem;

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

                        .trade-item {
                            .wl(50%, 2rem);
                        }
                    }
                }
            }
        }

        .section-two {
            .head-title {
                .fz(.2rem);
                padding-left: .4rem;
                padding-bottom: .2rem;
            }
            .order-chart {
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
                    <button class="action-btn withdraw">
                        提现申请 21
                    </button>
                    <button class="action-btn charge">
                        余额充值 21
                    </button>
                    <button class="action-btn margin">
                        保证金处理 13
                    </button>
                    <button class="action-btn margin">
                        代发货 13
                    </button>

                </section>
            </section>

            <section class="section-one-block trade-data">
                <header class="head-title fcm">
                    交易数据
                </header>

                <ul class="trade-list">
                    <li class="trade-item">
                        今日交易额
                    </li>
                    <li class="trade-item">
                        今日订单数
                    </li>
                    <li class="trade-item">
                        今日交易额
                    </li>
                    <li class="trade-item">
                        今日交易额
                    </li>
                </ul>
            </section>
        </section>
        <section class="section-two">
            <header class="head-title fcm">
                订单数据
            </header>
            <section class="order-chart"></section>
        </section>

    </div>
</template>

<script>
    export default {
        name: "index",

        data() {
            return {}
        },

        components: {},

        computed: {},

        methods: {},

        created() {
        },
    }
</script>

