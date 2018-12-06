<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .bgw();
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <ul class="nav-bar">
            <li v-for="item in recordType" :class="{'nav-bar-item': true, 'active': item.value == selectStatus}"
                @click="switchRecordType(item)">
                {{item.label}}({{item.num}})
            </li>
        </ul>

        <ul class="money-record">
            <li class="money-record-item" v-for="item in record">
                <p class="row">
                    <span class="hard">{{statusToTxt(item.CMstatus)}}</span>
                    <span class="weak">{{item.CMpaytime}}</span>
                </p>
                <p class="row">
                    <span class="weak">{{item.CMtradenum}}</span>
                    <span class="hard">￥{{item.CMamount}}</span>
                </p>
                <p class="reason" v-if="item.CMstatus == 3">
                    未通过原因:{{item.CMreason}}
                </p>
            </li>
        </ul>

    </div>
</template>

<script>
    import {getChargeMoneyList} from "src/api/api"

    //  充值记录
    export default {
        name: "chargeRecord",

        data() {
            return {
                selectStatus: 0,
                recordType: [
                    {
                        label: '全部',
                        value: 0,
                        num: 0
                    }, {
                        label: '待审核',
                        value: 1,
                        num: 0
                    }, {
                        label: '已充值',
                        value: 2,
                        num: 0
                    },{
                        label: '未通过',
                        value: 3,
                        num: 0
                    },
                ],

                record: [

                ]
            }
        },

        components: {
        },

        methods: {
            switchRecordType(item){
                this.selectStatus = item.value;
                this.setData();
            },
            statusToTxt(status){
                return this.recordType.find(item => item.value === status).label;
            },
            setData(){
                getChargeMoneyList(this.selectStatus).then(
                    resData => {
                        if (resData) {
                            if(this.selectStatus == 0){
                                this.recordType[0].num = resData.count0;
                                this.recordType[1].num = resData.count1;
                                this.recordType[2].num = resData.count2;
                                this.recordType[3].num = resData.count3;
                            }
                            this.record = resData.data;
                        }
                    }
                )
            }
        },

        created() {
            this.setData();
        }
    }
</script>

