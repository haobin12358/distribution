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
            padding: 20px 0 86px 20px;

            p:first-of-type {
                .fz(28px);
                text-indent: 0;
            }

            p {
                text-indent: 2em;
            }

        }
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true">
            <section slot="right">
                <router-link to="/chargeRecord" tag="img" src="/static/images/myOrder.png"
                             class="my-order-img"></router-link>
            </section>
        </header-top>

        <section class="form-container">
            <mt-field class="form-item" label="打款方式" placeholder="请选择打款方式" v-model="transferWay" :readonly="true"
                      :disableClear="true" @click.native="sheetVisible =true">
                <img src="/static/images/arrow_down.png" style="width: 16px;height: 14px;" alt="">
            </mt-field>
            <template v-if="formData.paytype == 1">
                <mt-field class="form-item" label="支付宝" v-model.trim="formData.alipaynum"
                          placeholder="请输入支付宝账号"></mt-field>
            </template>
            <template v-if="formData.paytype == 2">
                <mt-field class="form-item" v-model="formData.bankname" label="开户银行" placeholder="请输入开户银行"></mt-field>
                <mt-field class="form-item" v-model="formData.accountname" label="银行户名"
                          placeholder="请输入银行户名"></mt-field>
                <mt-field class="form-item" v-model="formData.cardnum" type="number" label="银行账号"
                          placeholder="请输入银行账号"></mt-field>
            </template>

            <!--<mt-field style="background: white;" label="打款日期" placeholder="请选择打款日期" v-model="date" :readonly="false" type="date" ></mt-field>-->

            <mt-field class="form-item" label="金额" v-model.trim.number="formData.amount" type="number"
                      placeholder="请输入打款金额"></mt-field>

            <template v-if="formData.paytype == 1 ||formData.paytype == 2 ">

                <mt-field class="form-item" label="打款日期" placeholder="请选择打款日期" :readonly="true" :disableClear="true"
                          v-model="date" @click.native="openDatePicker"></mt-field>
                <mt-field class="form-item" label="备注" v-model.trim="formData.remark"
                          placeholder="如有说明可填写备注"  @blur.native.capture="handleLastInputBlur"></mt-field>
                <evidence-field label="打款凭证(1-2张)" :readOnly="false" @update="updateEvdImg"
                                @isUploading="listenEvdUpload"
                                :upload-limit="2"></evidence-field>
            </template>
        </section>


        <section class="withdraw-tip">
            <p>请打款至：</p>

            <template v-if="formData.paytype == 1">
                <p>支付宝账号：{{registerInfo.alipaynum}}</p>
                <p>支付宝实名：{{registerInfo.alipayname}}</p>
            </template>
            <template v-if="formData.paytype == 2">
                <p>开户银行：{{registerInfo.bankname}}</p>
                <p>银行户名：{{registerInfo.accountname}}</p>
                <p>银行账号：{{registerInfo.cardnum}}</p>
            </template>
            <p>如有问题可联系微信客服：{{registerInfo.service}}</p>
        </section>

        <section v-if="formData.paytype == 1 || formData.paytype == 2" class="my-confirm-btn-wrap"
                 style="margin-top: 50px">
            <button v-if="isEvdImgUploading" class="my-confirm-btn disabled">凭 证 上 传 中...</button>
            <button v-else class="my-confirm-btn" @click="doConfirm">确 认 充 值</button>
        </section>

        <mt-actionsheet
            :actions="actions"
            v-model="sheetVisible">
        </mt-actionsheet>

        <mt-datetime-picker
            ref="picker"
            type="date"
            v-model="datetime"
            year-format="{value} 年"
            month-format="{value} 月"
            date-format="{value} 日"
            :closeOnClickModal="false"
            @cancel="close"
            :startDate="startDate"
            :endDate = "endDate"
            @confirm="dateTimeConfirm"
        >
        </mt-datetime-picker>
    </div>
</template>

<script>
    import {getRegisterInfo, chargeMonney, checkOpenid, title, weixinPay} from "src/api/api"
    import UploadField from "src/components/common/uploadField"
    import common from "src/common/js/common"
    import {mapState} from "vuex"
    import {setStore, getStore} from "src/common/js/mUtils"
    import {TOKEN} from "src/common/js/const"
    import TimeFormater from "time-formater";

    export default {
        name: "marginMoney",

        data() {
            return {
                transferWay: '支付宝',
                actions: [
                    // {name: '微信', value: 3, method: this.selectTransferWay},
                    {name: '支付宝', value: 1, method: this.selectTransferWay},
                    {name: '银行卡', value: 2, method: this.selectTransferWay},
                ],
                sheetVisible: false,
                datetime: new Date(),
                date: '',

                formData: {
                    "paytype": 1,
                    "alipaynum": "",
                    "bankname": "",
                    "accountname": "",
                    "cardnum": "",
                    "amount": 1,
                    "remark": "",
                    paytime: ''
                },
                registerInfo: {},

                startDate: new Date('2016'),
                endDate: new Date(),


                evidenceImgs: [],   //  凭证
                isEvdImgUploading: false,    //  凭证正在上传

            }
        },

        watch: {},

        computed: {
            ...mapState(['userInfo'])
        },


        components: {
            evidenceField: UploadField,
        },

        methods: {
            handleLastInputBlur(){
                window.scrollTo(0,0);
            },

            selectTransferWay(evt) {
                this.transferWay = evt.name;
                this.formData.paytype = evt.value;
            },

            openDatePicker() {
                this.closeTouch();
                this.$refs.picker.open();
            },
            dateTimeConfirm(evt) {
                this.openTouch();
                this.date = evt.toLocaleString('zh-CN', {hour12: false});
            },

            close() {
                this.openTouch();
            },

            /*解决页面层级相互影响滑动的问题*/
            handler: function (e) {
                e.preventDefault()
            },
            closeTouch() {
                document.getElementsByTagName('body')[0].addEventListener('touchmove', this.handler, {passive: false})//阻止默认事件
            },
            openTouch() {
                document.getElementsByTagName('body')[0].removeEventListener('touchmove', this.handler, {passive: false})//打开默认事件
            },

            updateEvdImg(imgs) {
                this.evidenceImgs = imgs;
            },
            listenEvdUpload(bool) {
                this.isEvdImgUploading = bool;
            },

            formDataCheck() {
                //  支付宝
                if (this.formData.paytype == 1) {
                    this.formData.bankname = ''
                    this.formData.accountname = ''
                    this.formData.cardnum = ''
                    if (!this.formData.alipaynum) {
                        return '请输入支付宝账号'
                    }
                }
                if (this.formData.paytype == 2) {
                    this.formData.alipaynum = ''
                    if (!this.formData.bankname) {
                        return '请输入开户银行'
                    }
                    if (!this.formData.accountname) {
                        return '请输入银行户名'
                    }
                    if (!this.formData.cardnum) {
                        return '请输入银行账号'
                    }
                }

                if (!this.formData.amount) {
                    return '请输入打款金额'
                } else if (!(this.formData.amount >= 0.01 && /^[0-9]+([.]{1}[0-9]+){0,1}$/.test(this.formData.amount))) {
                    return '请输入合理的打款金额数字'
                }

                if (!this.date) {
                    return '请输入打款日期'
                } else {
                    this.formData.paytime = TimeFormater(new Date(this.date)).format('YYYYMMDD');
                }

                if (!this.evidenceImgs.length) {
                    return '请上传打款凭证';
                } else {
                    this.formData.proof = this.evidenceImgs.join(',');
                }


            },
            doConfirm() {
                let checkMsg = this.formDataCheck();

                window.scrollTo(0,0);
                if (checkMsg) {
                    this.$toast(checkMsg);
                } else {
                    chargeMonney(this.formData).then(
                        resData => {
                            if (resData) {
                                this.$toast(resData.message);
                                this.$router.push('/chargeRecord');
                            }
                        }
                    )
                }
            },
        },

        created() {
            getRegisterInfo('').then(
                resData => {
                    if (resData) {
                        this.registerInfo = resData.data;
                    }
                }
            )
        }
    }
</script>

