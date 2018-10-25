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
        <header-top :show-back="true">
            <section slot="right">
                <router-link to="/withdrawCashRecord" tag="img" src="/static/images/myOrder.png"
                             class="my-order-img"></router-link>
            </section>
        </header-top>

        <section v-if="status == 1" class="form-container">
            <mt-field class="form-item" label="扣款方式" placeholder="余额" v-model="transferWay" :readonly="true"
                      :disableClear="true"></mt-field>
            <mt-field class="form-item" label="金额" :placeholder="'￥'+marginMoney" :readonly="true"
                      :disableClear="true"></mt-field>
        </section>

        <section v-if="status == 2" class="form-container">
            <mt-field class="form-item" label="退款方式" placeholder="银行卡" :readonly="true"
                      :disableClear="true">
            </mt-field>
            <mt-field class="form-item" type="number" label="银行卡号" placeholder="请输入银行卡号">
            </mt-field>

            <mt-field class="form-item" label="金额" :placeholder="'￥'+marginMoney" :readonly="true"
                      :disableClear="true"></mt-field>

        </section>


        <section class="withdraw-tip" v-if="status == 1">
            <p>
                备注：
            </p>
            <p>
                在后续的过程中，代理没有乱价则在退代理的时候可以退还保证金。
            </p>
        </section>

        <section class="confirm-btn-wrap">
            <button v-if="status == 1" class="confirm-btn">提 交</button>
            <button v-if="status == 2 && !isAudit" class="confirm-btn">退 还</button>
            <button v-if="isAudit" class="confirm-btn disabled">退 还</button>
        </section>

        <mt-popup v-model="isAudit">
            <section class="popup-content">
                <img src="/static/images/toast_audit.png" alt="">
                <span>审核中...</span>
            </section>
        </mt-popup>
    </div>
</template>

<script>
    export default {
        name: "balanceCharge",

        data() {
            return {
                status: 2,
                isAudit: true,
                transferWay: '余额',
                marginMoney: '200',


            }
        },

        watch: {},


        components: {},

        methods: {
            selectTransferWay(evt) {
                this.transferWay = evt.name;
            },
            dateTimeConfirm(evt) {
                this.date = evt.toLocaleString('zh-CN', {hour12: false});
            },
            uploadFile() {
                console.log(this.$refs.file.files[0]);

            }
        },

        created() {

        }
    }
</script>

