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

                .upload-imgs {
                    .fj(flex-start);

                    .upload-imgs-item {
                        .wl(123px, 123px);
                        margin-right: 30px;
                        position: relative;

                        img.evidence-img {
                            .wl(100%, 100%);
                        }

                        .img-block-close {
                            position: absolute;
                            width: 40px;
                            height: 40px;
                            right: -20px;
                            top: -20px;
                        }

                    }

                    .upload-imgs-item-placeholder {
                        position: relative;
                        .wl(123px, 123px);
                        border: 2px dotted @lightFontColor;

                        img {
                            position: absolute;
                            left: 50%;
                            top: 50%;
                            transform: translate(-50%, -50%);
                            .wl(47px, 47px);
                        }

                        input[type=file] {
                            position: absolute;
                            width: 100%;
                            height: 100%;
                            left: 0;
                            top: 0;
                            opacity: 0;
                        }
                    }
                }

            }

        }

        .withdraw-tip {
            .sc(22px, @lightFontColor);
            .bgw();
            padding:  20px 0 86px 20px;

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

        <section class="form-container">
            <mt-field class="form-item" label="余额充值" placeholder="请选择打款方式" v-model="transferWay" :readonly="true"
                      :disableClear="true" @click.native="sheetVisible =true"></mt-field>
            <mt-field class="form-item" label="支付宝" placeholder="请输入支付宝账号"></mt-field>
            <mt-field class="form-item" label="金额" placeholder="请输入打款金额" type="number"></mt-field>
            <mt-field class="form-item" label="日期" placeholder="请输入打款日期" :readonly="true" :disableClear="true"
                      v-model="date" @click.native="$refs.picker.open()"></mt-field>
            <mt-field class="form-item" label="备注" placeholder="如有说明可填写备注" type="password"></mt-field>
            <section class="upload-evidence">
                <span class="label">打款凭证</span>
                <ul class="upload-imgs">
                    <li class="upload-imgs-item">
                        <img class="evidence-img" src="/static/images/testbg.jpg" alt="">


                        <img class="img-block-close" src="/static/images/close.png" alt="">
                    </li>
                    <li class="upload-imgs-item-placeholder ">
                        <img src="/static/images/img-placeholder.png" alt="">
                        <input class="picture-file" id="up-picture-file" type="file" accept="image/*" ref="file"
                               @change="uploadFile">
                    </li>
                </ul>
            </section>
        </section>


        <section class="withdraw-tip">
            <p>
                请打款至：
            </p>
            <p>
                支付宝账号：zhelishiwoluanxiede@136.com
            </p>
            <p>
                支付宝实名：某某某
            </p>
            <p>
                如有问题可联系微信客服：木木12345
            </p>
        </section>

        <mt-actionsheet
            :actions="actions"
            v-model="sheetVisible">
        </mt-actionsheet>

        <mt-datetime-picker
            ref="picker"
            type="datetime"
            v-model="datetime"
            @confirm="dateTimeConfirm"
        >
        </mt-datetime-picker>
    </div>
</template>

<script>
    export default {
        name: "balanceCharge",

        data() {
            return {
                transferWay: '',
                birthday: '',
                date: '',


                actions: [
                    {name: '支付宝', method: this.selectTransferWay},
                    {name: '微信', method: this.selectTransferWay},
                ],
                sheetVisible: false,
                datetime: ''

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

