<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .bgw();
        .least-full-screen();

        .month-picker {
            padding: 0 12px;
            margin-top: 22px;
            margin-bottom: 50px;
            .fj();
            align-items: center;

            .arrow-wrap {
                flex: 1;
                .arrow {
                    .wl(26px, 39px);
                }

                &:last-of-type{
                    .fj(flex-end);
                }
            }

            .date {
                .sc(39px, @mainColor);
                .fontc(39px);

            }
        }

        .sale-info-total {
            text-align: center;
            color: black;
            margin-bottom: 24px;
            border-bottom: 1px solid @mainFontColor;

            .row-one {
                .sc(80px, #303133);
                margin-bottom: 27px;

            }

            .row-two {
                .fj();
                /*margin-bottom: 33px;*/

                .money-item{
                    flex: 1;
                    border: 2px solid #DCDFE6;
                    padding: 10px 0;
                    .fjc();
                    .sc(32px, #303133);

                    .label{
                        margin-bottom: 10px;

                    }
                    .value{

                    }

                }
            }

            .row-three {
                .fj();
                padding: 0 115px;

                .title {
                    margin-bottom: 14px;
                }
                .value {
                    .fz(40px);
                    font-weight: bold;

                    .unit {
                        .fz(20px);
                        font-weight: normal;

                    }
                }
            }
        }

        .sale-record-list {
            .sale-record-item {
                padding: 18px 26px 28px 34px;
                .fj();
                align-items: center;
                color: black;
                border-bottom: 2px solid @mainFontColor;

                .customer-img {
                    .wl(80px, 80px);
                    border-radius: 50%;
                    margin-right: 30px;
                    border: 5px solid @mainColor;
                    box-sizing: border-box;
                }

                .customer-name {
                    flex: 1;
                }

                .sale-num {

                }
            }

        }

        .record-list-none-tip{
            text-align: center;
            .fz(28px);

        }
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <section class="month-picker">
            <section class="arrow-wrap" @click="prevMonth">
                <img src="/static/images/datepicker-left.png"  alt="" class="arrow">
            </section>
            <span class="date">{{pickerMonth}}</span>
            <section class="arrow-wrap" @click="nextMonth">
                <img src="/static/images/datepicker-right.png" alt="" class="arrow">
            </section>
        </section>

        <section class="sale-info-total">
            <p class="row-one">
                ￥{{saleDetail.myprofit || 0}}
            </p>
            <section class="row-two">
                <section class="money-item">
                    <span class="label">直推奖励</span>
                    <span class="value">￥{{saleDetail.reward || 0}}</span>
                </section>
                <section class="money-item">
                    <span class="label">销售量</span>
                    <span class="value">{{saleDetail.performance || 0}}</span>
                </section>
                <section class="money-item">
                    <span class="label">销售件数返点</span>
                    <span class="value">￥{{saleDetail.discount || 0}}</span>
                </section>
            </section>
        </section>

        <ul class="sale-record-list" v-if="rankList.length">
            <li class="sale-record-item" v-for="item in rankList">
                <img class="customer-img" v-lazy="item.USheadimg" alt="">

                <span class="customer-name">
                    {{item.USname}}
                </span>
                <span class="sale-num">业绩:{{item.performance}}件</span>
            </li>
        </ul>

        <p v-else class="record-list-none-tip">
            当月没有销售排行数据
        </p>

    </div>
</template>

<script>
    import {getAccount, getRankList} from "src/api/api"

    export default {
        name: "sale",

        data() {
            return {
                now: Date.now(),

                saleDetail: {},
                rankList: [],
            }
        },

        computed: {
            pickerMonth() {
                let nowDate = new Date(this.now);
                let month = nowDate.getFullYear() + '-' +(nowDate.getMonth() +1).toString().padStart(2,'0');

                return month;
            }
        },

        components: {},

        methods: {
            prevMonth() {
                this.now = new Date(this.now).setDate(-1);
                this.setData();
            },

            nextMonth() {
                this.now = new Date(this.now).setDate(32);
                this.setData();
            },
            setData() {
                let month = this.pickerMonth.replace('-', '');

                getAccount(month).then(
                    resData => {
                        if (resData) {
                            this.saleDetail = resData.data;
                        }
                    }
                );
                getRankList(month).then(
                    resData => {
                        if (resData) {
                            this.rankList = resData.data;
                        }
                    }
                );
            }
        },

        created() {
            this.setData();
        }
    }
</script>

