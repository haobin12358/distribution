<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();

        .form-container {
            margin-top: 10px;
            .bs(0, 3px, 6px);
            padding: 20px;
            .bgw();

        }
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <section class="form-container">
            <mt-field class="form-item" label="有效期限" placeholder="请选择有效期限" v-model="expireDateTxt" :readonly="true"
                      :disableClear="true" @click.native="sheetVisible =true"></mt-field>
            <mt-field class="form-item" type="number" v-model="count" label="可用次数"
                      placeholder="请输入可用次数" :state="checkNumber(count) ?  '' :'warning'"></mt-field>
        </section>

        <section class="my-confirm-btn-wrap">
            <button v-if="bailstatus == 1" @click="doConfirm" class="my-confirm-btn">确 认</button>
            <button v-if="bailstatus == 2"  class="my-confirm-btn disabled">还需缴纳保证金({{shouldPay}}元)</button>
            <button v-if="bailstatus == 3"  class="my-confirm-btn disabled">保证金退还中,无法新增邀请</button>
        </section>

        <mt-actionsheet
            :actions="actions"
            v-model="sheetVisible">
        </mt-actionsheet>
    </div>
</template>

<script>
    import {addQrcode} from "src/api/api"
    import common from "src/common/js/common"
    import {checkBail} from "src/api/api"


    export default {
        name: "newInvite",

        data() {
            return {
                expireDateTxt: '',  // 显示用
                expireDate: '',
                count: '',

                actions: [
                    {name: '一小时', method: this.selectExpiryDate},
                    {name: '一天', method: this.selectExpiryDate},
                    {name: '一周', method: this.selectExpiryDate},
                    {name: '一月', method: this.selectExpiryDate},
                ],
                sheetVisible: false,

                bailstatus: 1,
                shouldPay: 0
            }
        },

        components: {},

        computed: {},

        methods: {
            checkNumber(number){
                let reg = /^[1-9]+[0-9]*]*$/;
                if(!number){
                    return true;
                }
                return reg.test(number);
            },
            selectExpiryDate(evt) {
                this.expireDateTxt = evt.name;

            },

            expireDateTxtToVal(){
                switch (this.expireDateTxt) {
                    case '一小时':
                        this.expireDate = new Date().getTime() + 60 * 60 * 1000;
                        break;
                    case '一天':
                        this.expireDate = new Date().getTime() + 24 * 60 * 60 * 1000;
                        break;
                    case '一周':
                        this.expireDate = new Date().getTime() + 7 * 24 * 60 * 60 * 1000;
                        break;
                    case '一月':
                        this.expireDate = new Date().getTime() + 30 * 24 * 60 * 60 * 1000;
                        break;
                }

                let tempDate = new Date(Number(this.expireDate));

                this.expireDate = common.dateFormat(tempDate);
            },

            doConfirm() {
                if (this.expireDateTxt && this.count > 0) {

                    this.expireDateTxtToVal();

                    addQrcode(this.expireDate, this.count).then(
                        resData => {
                            if(resData){
                                this.$toast('邀请新增成功');
                                this.$router.back();
                            }
                        }
                    )
                } else {
                    this.$toast('请填写完整!');
                }
            }
        },

        async created() {
            let checkData = await checkBail();

            this.bailstatus = checkData.bailstatus;
            this.shouldPay = checkData.data.shouldpay;
        },
    }
</script>

