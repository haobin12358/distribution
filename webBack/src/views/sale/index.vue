<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .sale-data-list{
            .fj();

            .sale-data-item{
                .wl(2.5rem, 2rem);
                padding: .3rem 0 .4rem;
                box-sizing: border-box;
                .fjc();
                align-items: center;
                border: 1px solid #46a0fc;

                &.active{
                    border-top: .1rem solid #46a0fc;

                }

                .num{
                    .sc(.4rem, #46a0fc);

                }

                .title{
                    text-align: center;

                }


            }
        }
    }
</style>

<template>
    <div class="container">
        <h1 class="my-title">
            销售数据
        </h1>
        <ul class="sale-data-list">
            <li class="sale-data-item active">
                <span class="num">158741</span>
                <span class="title">总销售量（件）</span>

            </li>
            <li class="sale-data-item ">
                <span class="num">￥15778.00</span>
                <span class="title">总销售额（元）</span>

            </li>
            <li class="sale-data-item ">
                <span class="num">45478</span>
                <span class="title">订单数（笔）</span>

            </li>
            <li class="sale-data-item ">
                <span class="num">158741</span>
                <span class="title">总代理数（人）</span>

            </li>

            <li class="sale-data-item ">
                <span class="num">￥158.00</span>
                <span class="title">客单价（元）</span>

            </li>
            <li class="sale-data-item ">
                <span class="num">158741</span>
                <span class="title">新增代理数（人）</span>

            </li>
        </ul>

        <h1 class="my-title">
            数据趋势
        </h1>
        <section>
            图表
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

