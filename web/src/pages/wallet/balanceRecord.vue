<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();

        .balance-record-list {
            margin-top: 10px;
            .balance-record-item {
                .bgw();
                .bs(10px, 3px, 6px);
                padding: 0 20px;

                .record-hd {
                    padding: 22px 6px 16px;
                    border-bottom: 1px solid @grayBorderColor;
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
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <!--<ul class="nav-bar">-->
            <!--<li v-for="item in recordType" :class="{'nav-bar-item': true, 'active': item.value == selectStatus}"-->
                <!--@click="switchRecordType(item)">-->
                <!--{{item.label}}({{item.num}})-->
            <!--</li>-->
        <!--</ul>-->
        <!---->
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

                    <p v-if="item.MRtype == 1 || item.MRtype == 8">订单号：{{item.OIid}}</p>
                    <p v-else>流水号：{{item.MRtradenum}}</p>
                </section>
            </li>
        </ul>
    </div>
</template>

<script>
    import moneyRecord from "src/components/common/moneyRecord"
    import {getMoneyRecord} from "src/api/api"


    export default {
        name: "balanceRecord",

        data() {
            return {
                selectStatus: 0,
                // recordType: [
                //     {
                //         label: '全部',
                //         value: 0,
                //         num: 0
                //     }, {
                //         label: '待审核',
                //         value: 1,
                //         num: 0
                //     }, {
                //         label: '已充值',
                //         value: 2,
                //         num: 0
                //     },{
                //         label: '未通过',
                //         value: 3,
                //         num: 0
                //     },
                // ],

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
                    },{
                        value: 8,
                        label: '订单退还'
                    }
                ],
                moneyRecord: []
            }
        },

        components: {
            moneyRecord
        },

        methods: {
            switchRecordType(item){
                this.selectStatus = item.value;
                // this.setData();
            },

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
            this.setMoneyRecord();
        }
    }
</script>

