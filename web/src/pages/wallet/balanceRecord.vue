<style lang="less" scoped>
    @import "../../common/css/index";

    .container{
        .bgw();
    }
</style>

<template>
    <div class="container">
        <header-top :title="$route.meta.title" :show-back="true">
        </header-top>

        <mt-navbar v-model="selected" style="margin-bottom: 10px">
            <mt-tab-item id="1">全部 (17)</mt-tab-item>
            <mt-tab-item id="2">待审核 (1)</mt-tab-item>
            <mt-tab-item id="3">待打款 (1)</mt-tab-item>
            <mt-tab-item id="4">已打款 (1)</mt-tab-item>
            <mt-tab-item id="5">未通过 (1)</mt-tab-item>
        </mt-navbar>

        <mt-tab-container v-model="selected" :swipeable="true">
            <mt-tab-container-item id="1">
                <money-record :list="record" @clickItem.user="$router.push({path: '/balanceRecordDetail', query:$event})"></money-record>
            </mt-tab-container-item>
            <mt-tab-container-item id="2">
                <money-record :list="record" @clickItem.user="$router.push({path: '/balanceRecordDetail', query:$event})"></money-record>
            </mt-tab-container-item>
            <mt-tab-container-item id="3">
                <money-record :list="record" @clickItem.user="$router.push({path: '/balanceRecordDetail', query:$event})"></money-record>
            </mt-tab-container-item>

        </mt-tab-container>
    </div>
</template>

<script>
    import moneyRecord from "src/components/common/moneyRecord"

    export default {
        name: "balanceRecord",

        data() {
            return {
                selected: '1',

                record: [
                    {
                        type: '新代理',
                        date: '2018-07-21',
                        sn: '流水号：123547998779',
                        price: '￥10.00',
                    },{
                        type: '新代理',
                        date: '2018-07-21',
                        sn: '流水号：123547998779',
                        price: '￥10.00',
                    },{
                        type: '新代理',
                        date: '2018-07-21',
                        sn: '流水号：123547998779',
                        price: '￥10.00',
                    },
                ]
            }
        },

        components: {
            moneyRecord
        },

        methods: {},
    }
</script>

