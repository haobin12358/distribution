<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .bgw();

        .month-picker {
            padding: 0 211px;
            margin-top: 22px;
            margin-bottom: 50px;
            .fj();
            align-items: center;

            .arrow {
                .wl(20px, 30px);
            }

            .date {
                color: @mainColor;
                .fontc(30px);

            }
        }

        .sale-info-total {
            text-align: center;
            color: black;
            /*margin-bottom: 54px;*/
            border-bottom: 1px solid @mainFontColor;

            .row-one {
                .sc(80px, black);
                font-weight: bold;
                margin-bottom: 27px;

                .unit {
                    .fz(40px);
                }
            }

            .row-two {
                .fj();
                padding: 0 115px;
                margin-bottom: 33px;

                .row-two-section {
                    .title {
                        margin-bottom: 14px;
                    }
                    .value {
                        .fz(40px);
                        font-weight: bold;
                        margin-bottom: 33px;

                    }

                    .sale-num-title, .sale-num-value {
                        line-height: 44px;
                        color: #F56C6C;

                    }
                    .sale-num-value{
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
                border-bottom: 1px solid @mainFontColor;

                .customer-img{
                    .wl(80px, 80px);
                    border-radius: 50%;
                    margin-right: 30px;
                    border: 5px solid @mainColor;
                    box-sizing: border-box;
                }

                .customer-name{
                    flex: 1;
                }

                .sale-num{

                }
            }

        }
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <section class="month-picker">
            <img src="/static/images/datepicker-left.png" @click="prevMonth" alt="" class="arrow">
            <span class="date">{{pickerMonth}}</span>
            <img src="/static/images/datepicker-right.png" @click="nextMonth" alt="" class="arrow">
        </section>

        <section class="sale-info-total">
            <p class="row-one">
                <span class="unit">￥</span>{{saleDetail.myprofit || 0}}
            </p>
            <section class="row-two">
                <section class="row-two-section">
                    <p class="title">直推奖励</p>
                    <p class="value">{{saleDetail.reward || 0}}</p>
                    <p class="sale-num-title title">销售量</p>

                </section>
                <section class="row-two-section">
                    <p class="title">销售件数返点</p>
                    <p class="value">{{saleDetail.discount || 0}}</p>
                    <p class="sale-num-value value">{{saleDetail.performance || 0}}<span class="unit">件</span></p>
                </section>
            </section>
        </section>

        <ul class="sale-record-list">
            <li class="sale-record-item" v-for="item in rankList">
                <img class="customer-img" :src="item.USheadimg" alt="">

                <span class="customer-name">
                    {{item.USname}}
                </span>
                <span class="sale-num">业绩:{{item.performance}}件</span>
            </li>
        </ul>
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

        computed:{
          pickerMonth(){
              let nowDate = new Date(this.now);
              let month = nowDate.getFullYear() + '-' ;

              if(nowDate.getMonth()+1 < 10){
                  month += '0'+ (nowDate.getMonth()+1);
              }else{
                  month += (nowDate.getMonth()+1);
              }

              return month;
          }
        },

        components: {},

        methods: {
            prevMonth(){
                this.now = new Date(this.now).setDate(-1);
                this.setData();
            },

            nextMonth(){
                this.now = new Date(this.now).setDate(32);
                this.setData();
            },
            setData(){
                let month = this.pickerMonth.replace('-', '');

                getAccount(month).then(
                    resData => {
                        if(resData){
                            this.saleDetail = resData.data;
                        }
                    }
                );
                getRankList(month).then(
                    resData => {
                        if(resData){
                            this.rankList = resData.data;
                        }
                    }
                );
            }
        },

        created(){
            this.setData();
        }
    }
</script>

