<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();

        .bank-balance {
            background: white;
            padding: 48px 20px 16px;
            .bs(10px, 3px, 6px);

            .bank-balance-hd {
                padding: 0 20px 26px;

                .row-one {
                    margin-bottom: 41px;
                    .fj();
                    align-items: center;
                    .fz(26px);

                    .margin-money {
                        .margin-money-num {
                            .sc(32px, @moneyColor)
                        }
                    }
                }

                .num {
                    .sc(80px, @moneyColor);
                    font-weight: bold;
                }
            }

            .bank-balance-charge {
                padding: 20px 5px 20px 20px;
                border-top: 2px solid @grayBorderColor;
                border-bottom: 2px solid @grayBorderColor;
                .fj();
                align-items: center;
                .fz(26px);

                .left {

                }
                .right {
                    .wl(15px, 26px);
                }
            }

            .bank-balance-ft {
                .fj(flex-end);
                padding-top: 22px;

                .go-balance-record {
                    .sc(26px, @mainColor);
                    .wl(140px, 40px);
                    .fontc(28px);
                    background: white;
                    .bd(@mainColor, 30px);
                }
            }
        }

        .balance-record-list {
            .balance-record-item {
                .bgw();
                .bs(10px, 3px, 6px);
                padding: 0 20px;

                .record-hd {
                    padding: 22px 6px 16px;
                    border-bottom: 2px solid @grayBorderColor;
                    .fj();

                    .type {
                        .fz(28px);
                    }

                    .date {
                        .sc(18px, @lightFontColor);
                    }
                }

                .record-bd {
                    padding: 19px 6px 41px;
                    color: @lightFontColor;

                    .price {
                        margin-bottom: 15px;
                    }
                    .order-no {
                    }

                }

                &:last-of-type {
                    margin-bottom: 144px;
                }
            }
        }

        .record-list-none{
            text-align: center;
            .sc(26px, #cccccc);
        }
    }
</style>

<template>
    <div class="container">
        <header-top :title="$route.meta.title" :showBack="true">
            <section slot="right">
                <router-link tag="button" to="/withdrawCash" class="header-btn">提现</router-link>
            </section>
        </header-top>

        <section class="bank-balance">
            <header class="bank-balance-hd">
                <p class="row-one">
                    <span>
                        账户余额（元）
                    </span>
                    <router-link to="/marginMoney" tag="section" class="margin-money">
                        <span class="">保证金</span>
                        <span class="margin-money-num">￥0.00</span>
                    </router-link>
                </p>
                <p class="num">￥{{userInfo.USmount}}</p>
            </header>

            <router-link to="/balanceCharge" tag="section" class="bank-balance-charge">
                <span>余额充值</span>
                <img src="/static/images/arrow.png" class="right" alt="">
            </router-link>

            <footer class="bank-balance-ft">
                <router-link to="/balanceRecord" tag="button" class="go-balance-record">收支记录</router-link>
            </footer>
        </section>

        <template v-if="moneyRecord.length">

            <ul class="balance-record-list">
                <li class="balance-record-item" v-for="item in moneyRecord">
                    <header class="record-hd">
                    <span class="type">
                        类型：{{statusToTxt(item.MRtype)}}
                    </span>
                        <span class="date">
                        {{item.MRcreatetime}}
                    </span>
                    </header>

                    <section class="record-bd">
                        <p class="price">金额：{{item.MRamount}}</p>
                        <p v-if="item.MRtype == 1">订单号：{{item.MRtradenum}}</p>
                        <p v-else>流水号：{{item.MRtradenum}}</p>
                    </section>
                </li>
            </ul>
            <load-more></load-more>
        </template>
        <p v-else class="record-list-none">
            有余额变动的收支记录会显示在这
        </p>
    </div>
</template>

<script>
    import {mapState, mapActions, mapMutations} from "vuex"
    import {getMoneyRecord} from "src/api/api"


    export default {
        name: "wallet",

        data() {
            return {
                recordType: [
                    {
                        value: 1,
                        label: '订单支出'
                    }, {
                        value: 2,
                        label: '提现'
                    }, {
                        value: 3,
                        label: '充值保证金'
                    }, {
                        value: 4,
                        label: '余额充值'
                    }, {
                        value: 5,
                        label: '奖金发放'
                    }, {
                        value: 6,
                        label: '保证金退还'
                    }, {
                        value: 7,
                        label: '提现失败'
                    },
                ],
                moneyRecord: []
            }
        },

        components: {},

        computed: {
            ...mapState(['userInfo']),

        },

        methods: {
            ...mapActions(['getUserInfo']),

            setMoneyRecord() {
                getMoneyRecord().then(
                    resData => {
                        if (resData) {
                            this.moneyRecord = resData.data;
                        }
                    }
                )
            },

            statusToTxt(status){
                return this.recordType.find(item => item.value == status).label;
            }
        },

        created() {
            this.getUserInfo();
            this.setMoneyRecord();
        }
    }
</script>

