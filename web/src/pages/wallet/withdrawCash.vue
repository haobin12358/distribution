<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();

        .form-container {
            margin-top: 10px;
            .bs(0, 3px, 6px);
            padding: 20px;
            .bgw();

            .form-item {
            }

        }

        .confirm-btn-wrap {
            margin-top: 343px;
            .fj(center);

            .confirm-btn {
                .wl(600px, 90px);
                .fontc(90px);
                font-weight: bold;
                background: linear-gradient(180deg, @mainLightColor 0%, @mainColor 100%);
                .sc(38px, white);
                border-radius: 50px;

            }
        }
    }
</style>

<template>
    <div class="container">
        <header-top :title="$route.meta.title" :show-back="true">
            <section slot="right">
                <router-link to="/withdrawCashRecord" tag="img" src="/static/images/myOrder.png"
                             class="my-order-img"></router-link>
            </section>
        </header-top>

        <section class="form-container">
            <mt-field class="form-item" label="银行名称" v-model="formData.bankname" :readonly="true" :disableClear="true"
                      placeholder="请输入银行名称"></mt-field>
            <mt-field class="form-item" label="支行名称" v-model.trim="formData.branchbank" placeholder="请输入支行名称"></mt-field>
            <mt-field class="form-item" label="开户姓名" v-model="formData.accountname" :readonly="true" :disableClear="true"
                      placeholder="请输入开户姓名"></mt-field>
            <mt-field class="form-item" label="卡号" v-model="formData.cardnum" type="number"
                      placeholder="请输入卡号"></mt-field>
            <mt-field class="form-item" label="金额" v-model="formData.amount" type="number" :disableClear="false"
                      placeholder="请输入金额"></mt-field>
        </section>

        <section class="confirm-btn-wrap">
            <button class="confirm-btn" @click="doConfirm">确 认 提 现</button>
        </section>

    </div>
</template>

<script>
    import {getDrawInfo, drawMoney} from "src/api/api"
    import {mapActions} from "vuex"


    export default {
        name: "withdrawCash",

        data() {
            return {
                formData: {
                    bankname: '',
                    branchbank: '',
                    accountname: '',
                    cardnum: '',
                    amount: '',
                }
            }
        },

        components: {},

        methods: {

            formDataCheck(){
                if(!this.formData.branchbank){
                    return '请输入支行名称!';
                }
                if(!this.formData.cardnum){
                    return '请输入银行卡号!';
                }
                if(!this.formData.amount){
                    return '请输入合理的打款金额数字';
                }else if(!(this.formData.amount >= 0.01 && /^[0-9]+([.]{1}[0-9]+){0,1}$/.test(this.formData.amount))){
                    return '请输入合理的打款金额数字'
                }


            },
            doConfirm(){
                let checkMsg = this.formDataCheck();

                if(checkMsg){
                    this.$toast(checkMsg);
                }else{
                    this.$messagebox.confirm(`确认提现${this.formData.amount}元?`).then(
                        ()=>{
                            drawMoney(this.formData).then(
                                resData => {
                                    if (resData) {
                                        this.$toast(resData.message);
                                        this.$router.push('/withdrawCashRecord');
                                    }
                                }
                            )
                        }
                    )
                }
            },

        },

        created() {
            getDrawInfo().then(
                resData => {
                    if (resData) {
                        this.formData.bankname = resData.data.bankname;
                        this.formData.accountname = resData.data.username;
                    }
                }
            )
        }
    }
</script>

