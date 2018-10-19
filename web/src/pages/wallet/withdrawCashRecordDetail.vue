<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();
        .bgw();


        .record-list{
            margin-top: 10px;

            .record-item{
                padding: 7px 26px 0 37px;
                margin-bottom: 20px;
                .fj();
                .fz(30px);

                .title{
                    color: #999999;
                    white-space: nowrap;

                }

                .value{
                    color: black;

                }
            }
        }
    }
</style>

<template>
    <div class="container">
        <header-top :title="$route.meta.title" :show-back="true"></header-top>

        <ul class="record-list">
            <li class="record-item">
                <span class="title">流水号：</span>
                <span class="value">123547998779152</span>
            </li>
            <li class="record-item">
                <span class="title">类型：</span>
                <span class="value">订单支出</span>
            </li>
            <li class="record-item">
                <span class="title">支出：</span>
                <span class="value">￥10.00</span>
            </li>
            <li class="record-item">
                <span class="title">支付方式：</span>
                <span class="value">余额</span>
            </li>
            <li class="record-item">
                <span class="title">时间：</span>
                <span class="value">2018-09-10  08:05:13</span>
            </li>
            <li class="record-item">
                <span class="title">余额：</span>
                <span class="value">￥1500.00</span>
            </li>
            <li class="record-item">
                <span class="title">备注：</span>
                <span class="value">购买了帮宝适A款12袋</span>
            </li>

        </ul>
    </div>
</template>

<script>
    export default {
        name: "withdrawCashRecordDetail",

        data() {
            return {}
        },

        components: {},

        methods: {},

        created() {
            console.log('[query]');
            console.log(this.$route.query);
        }
    }
</script>

