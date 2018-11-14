<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();

        .form-container {
            margin-top: 10px;
            .bs(0, 3px, 6px);
            padding: 20px;
            border-bottom: 1px solid @grayBorderColor;
            .bgw();

            .form-item {

            }

            .upload-evidence {
                margin-left: 24px;
                padding-top: 24px;
                border-top: 1px solid @grayBorderColor;
                .fj(flex-start);

                .label {
                    font-size: 32px;
                    margin-right: 36px;

                }

            }

        }

        .withdraw-tip {
            .sc(22px, @lightFontColor);
            .bgw();
            padding: 20px 0 86px 20px;

        }

        .popup-content {
            width: 340px;
            height: 420px;
            .bgw();
            border-radius: 50px;
            .fj();
            flex-direction: column;
            align-items: center;
            padding: 80px;
            box-sizing: border-box;
            .sc(38px, @mainColor);
            font-weight: bold;

            img {
                .wl(169px, 169px);
            }
        }

    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <template v-if="bailstatus == 2">
            <section class="form-container">
                <mt-field class="form-item" label="扣款方式" :value="transferWay" :readonly="true"
                          :disableClear="true"></mt-field>
                <mt-field class="form-item" label="保证金额" :value="'￥'+shouldPay" :readonly="true"
                          :disableClear="true"></mt-field>
            </section>

            <section class="withdraw-tip">
                <p>
                    备注：
                </p>
                <p>
                    在后续的过程中，代理没有乱价则在退代理的时候可以退还保证金。
                </p>
            </section>
        </template>

        <section v-if="bailstatus == 1 || bailstatus == 3" class="form-container">
            <mt-field class="form-item" label="退款方式" :value="transferWay" :readonly="true"
                      :disableClear="true">
            </mt-field>
            <mt-field class="form-item" label="已交金额" :value="'￥'+personBail" :readonly="true"
                      :disableClear="true"></mt-field>

        </section>


        <section class="my-confirm-btn-wrap">
            <button v-if="bailstatus == 1" @click="returnMarginMoney" class="my-confirm-btn">退 还</button>
            <button v-if="bailstatus == 2" @click="payMarginMoney" class="my-confirm-btn">提 交</button>
            <button v-if="bailstatus == 3" class="my-confirm-btn disabled">退 还 审 核 中...</button>
        </section>

        <!--<mt-popup v-model="isAudit">-->
        <!--<section class="popup-content">-->
        <!--<img src="/static/images/toast_audit.png" alt="">-->
        <!--<span>审核中...</span>-->
        <!--</section>-->
        <!--</mt-popup>-->
    </div>
</template>

<script>
    import {checkBail, chargeDrawBail, getUserBasicInfo} from "src/api/api"

    export default {
        name: "balanceCharge",

        data() {
            return {
                transferWay: '余额',
                bailstatus: 3,
                shouldPay: 100,
                personBail: 0
            }
        },

        watch: {},


        components: {},

        methods: {
            returnMarginMoney() {
                if(this.personBail > 0){

                    this.$messagebox.confirm(`退还保证金后无法下单和邀请代理,确认退还(${this.personBail}元)?`).then(
                        () => {
                            chargeDrawBail(2, this.personBail).then(
                                resData => {
                                    if (resData) {
                                        this.$toast('您的退还申请已进入审核');
                                        this.$router.back();
                                    }
                                }
                            )
                        }
                    )
                }else{
                    this.$toast('当前金额无法退还');
                }
            },
            payMarginMoney() {
                this.$messagebox.confirm(`缴纳保证金后可以下单和邀请代理,确认缴纳(${this.shouldPay}元)?`).then(
                    () => {
                        chargeDrawBail(2, this.personBail).then(
                            resData => {
                                if (resData) {
                                    chargeDrawBail(1, this.shouldPay).then(
                                        resData => {
                                            if (resData) {
                                                this.$toast('缴纳保证金成功');
                                                this.$router.back();
                                            }
                                        }
                                    )
                                }
                            }
                        )
                    }
                )

            }
        },

        async created() {
            let checkData = await checkBail();

            // console.log('获取保证金');
            this.bailstatus = checkData.bailstatus;

            if (this.bailstatus == 1) {
                let {data} = await getUserBasicInfo();

                this.personBail = data.USbail;
            }else if(this.bailstatus == 2){
                this.shouldPay = checkData.data.shouldpay;
            }
        },
    }
</script>

