<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .inviter-info {
            margin-top: 10px;
            .bs(10px, 3px, 6px);
        }

        .form-title {
            height: 70px;
            line-height: 70px;
            padding-left: 22px;
            .fz(34px);
            font-weight: bold;
            color: @lightFontColor;

        }
        input:focus {
            background: yellow;
        }
        .main-form {
            .get-qrcode-btn {
                width: 157px;
                height: 40px;
                border: 2px solid @mainColor;
                border-radius: 30px;
                .fontc(40px);
                .fz(24px);
                background: white;
            }

        }

        .city-picker-popup {
            width: 100%;

            .city-picker-toolbar {
                .fj();
                padding: 10px 60px;

                button {
                    .bgw();
                    .sc(38px, #26b83a);

                    &.cancel-btn {
                        color: @lightFontColor;
                    }
                }
            }
        }
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <section class="inviter-info">
            <my-cell style="text-align: right" title="邀请代理" :value="formData.preusername" :readonly="true"></my-cell>
            <my-cell style="text-align: right" title="联系电话" :value="formData.prephonenum" :readonly="true"></my-cell>
            <my-cell style="text-align: right" title="联系地址" :value="registerInfo.address"
                     :readonly="true"></my-cell>
        </section>

        <section class="form-title">
            填写内容
        </section>

        <section class="main-form">
            <mt-field label="姓名" v-model.trim="formData.username" placeholder="请输入姓名"></mt-field>
            <mt-field label="联系电话" v-model.lazy.number="formData.phonenum" onkeyup="value=value.replace(/[^\d]/g,'')" type="tel" placeholder="请输入联系电话"></mt-field>
            <mt-field label="验证码" v-model.trim="formData.inforcode" placeholder="请输入验证码">
                <button class="get-qrcode-btn" :disabled="lastEnableCodeSecond>0" @click="getCode">
                    {{lastEnableCodeSecond>0 ?`剩余${lastEnableCodeSecond}s`: '获取'}}
                </button>
            </mt-field>
            <mt-field label="密码" v-model="formData.password" type="password" placeholder="请输入登录密码"></mt-field>
            <mt-field label="密码确认" v-model="passwordConfirm" type="password" placeholder="请再次输入登录密码"></mt-field>
            <mt-field label="微信号" v-model.trim="formData.wechat" placeholder="请输入微信号"></mt-field>
            <mt-field label="身份证号" v-model.trim="formData.idcardnum" placeholder="请输入身份证号"></mt-field>
            <mt-field label="省市区" placeholder="请选择省市区" v-model="city" :readonly="true"
                      :disableClear="true" @click.native="showCityPopup">
                <img src="/static/images/arrow_down.png" style="width: 16px;height: 14px;" alt="">
            </mt-field>
            <mt-field label="详细地址" v-model.trim="formData.details" placeholder="请输入详细地址"></mt-field>

            <mt-field class="form-item" label="打款方式" placeholder="请选择打款方式" v-model="transferWay " :readonly="true"
                      :disableClear="true" @click.native="showTransferWay">
                <img src="/static/images/arrow_down.png" style="width: 16px;height: 14px;" alt="">
            </mt-field>
            <mt-field class="form-item" label="金额" :value="registerInfo.money" :readonly="true"
                      placeholder="请输入打款金额"></mt-field>

            <template v-if="formData.paytype == 1">
                <mt-field class="form-item" v-model.trim="formData.alipaynum" label="支付宝" placeholder="请输入支付宝账号"></mt-field>
            </template>
            <template v-if="formData.paytype == 2">
                <mt-field class="form-item" v-model.trim="formData.bankname" label="开户银行" placeholder="请输入开户银行"></mt-field>
                <mt-field class="form-item" v-model.trim="formData.accountname" label="银行户名"
                          placeholder="请输入银行户名"></mt-field>
                <mt-field class="form-item" v-model.trim="formData.cardnum" type="number" label="银行账号"
                          placeholder="请输入银行账号"></mt-field>
            </template>


            <mt-field class="form-item" label="打款日期" placeholder="请选择打款日期" :readonly="true" :disableClear="true"
                      v-model="date" @click.native="openDatePicker"></mt-field>
            <head-img-field label="新头像" :readOnly="false" @update="updateNewHeadImg" @isUploading="listenHdUpload"
                            :upload-limit="1" type="1"></head-img-field>
            <evidence-field label="打款凭证(1-2张)" :readOnly="false" @update="updateEvdImg" @isUploading="listenEvdUpload"
                            :upload-limit="2"></evidence-field>
        </section>

        <section class="form-title">
            请打款至
        </section>


        <section class="inviter-info">
            <template v-if="formData.paytype == 1">
                <my-cell style="text-align: right" title="支付宝账号" :value="registerInfo.alipayname"
                         :readonly="true"></my-cell>
                <my-cell style="text-align: right" title="支付宝实名" :value="registerInfo.alipaynum"
                         :readonly="true"></my-cell>
            </template>
            <template v-if="formData.paytype == 2">
                <my-cell style="text-align: right" title="开户银行" :value="registerInfo.bankname"
                         :readonly="true"></my-cell>
                <my-cell style="text-align: right" title="银行户名" :value="registerInfo.accountname"
                         :readonly="true"></my-cell>
                <my-cell style="text-align: right" title="银行账号" :value="registerInfo.cardnum"
                         :readonly="true"></my-cell>
            </template>

            <my-cell style="text-align: right" title="如有问题请联系微信客服" :value="registerInfo.service" :readonly="true"></my-cell>
        </section>

        <section class="my-confirm-btn-wrap" style="margin: 30px 0 60px;">
            <button v-if="isHdImgUploading || isEvdImgUploading" class="my-confirm-btn disabled">图 片 上 传 中...</button>
            <button v-else class="my-confirm-btn" @click="doConfirm">确 认</button>
        </section>

        <mt-popup class="city-picker-popup" position="bottom" v-model="cityPopupVisible">
            <mt-picker :slots="slots" defaultIndex="2" valueKey="name" @change="onValuesChange" :showToolbar="true">
                <section class="city-picker-toolbar">
                    <button class="cancel-btn" @click="cityPopupVisible= false">取消</button>
                    <button @click="confirmPickArea">确认</button>
                </section>
            </mt-picker>
        </mt-popup>


        <mt-actionsheet
            :actions="transferWayActions"
            v-model="twSheetVisible">
        </mt-actionsheet>


        <mt-datetime-picker
            ref="picker"
            type="datetime"
            month-format="{value} 月"
            date-format="{value} 日"
            hour-format="{value} 时"
            minute-format="{value} 分"
            v-model="datetime"
            :startDate = "startDate"
            :endDate = "endDate"
            :closeOnClickModal="false"
            @cancel="closeDatePicker"
            @confirm="dateTimeConfirm"
        >
        </mt-datetime-picker>
    </div>
</template>

<script>
    import myCell from "src/components/common/myCell"
    import {getInforcode, getAllArea, getRegisterInfo, register} from "src/api/api"
    import {setStore, getStore} from "src/common/js/mUtils"
    import common from "src/common/js/common"
    import {ALL_AREA} from "src/common/js/const"
    import UploadField from "src/components/common/uploadField"
    import TimeFormater from "time-formater";

    export default {
        name: "applyAgent",

        data() {
            return {
                transferWay: '支付宝',
                date: '',
                datetime: new Date(),
                startDate: new Date('2016'),
                endDate: new Date(),

                timer: null,    //  计时器
                lastEnableCodeSecond: 0,    //  下一次可用验证码倒计时

                registerInfo: {},

                formData: {
                    // qrid: '',
                    preusername: "",
                    prephonenum: "",
                    username: '',
                    phonenum: '',
                    inforcode: '',
                    password: '',
                    idcardnum: '',
                    wechat: '',
                    cityid: '',
                    areaid: '',
                    details: '',
                    paytype: 1,
                    paytime: '',
                    headimg: '',
                    proof: '',
                    alipaynum: "",
                    bankname: '',
                    accountname: '',
                    cardnum: '',
                    payamount: ''
                },

                passwordConfirm: '',

                transferWayActions: [
                    {name: '支付宝', type: 1, method: this.selectTransferWay},
                    {name: '银行转账', type: 2, method: this.selectTransferWay},
                ],
                twSheetVisible: false,


                city: '',
                cityPopupVisible: false,
                allArea: [],
                slots: [
                    {
                        flex: 1,
                        values: [],
                        className: 'slot1',
                        textAlign: 'center'
                    }, {
                        divider: true,
                        content: '-',
                        className: 'slot2'
                    }, {
                        flex: 1,
                        values: [],
                        className: 'slot3',
                        textAlign: 'center'
                    }
                    , {
                        divider: true,
                        content: '-',
                        className: 'slot4'
                    }, {
                        flex: 1,
                        values: [],
                        className: 'slot5',
                        textAlign: 'center'
                    }
                ],
                pickAreaVal: [],


                headImgs: [],   //  头像
                isHdImgUploading: false,    //  头像正在上传

                evidenceImgs: [],   //  凭证
                isEvdImgUploading: false,    //  凭证正在上传
            }
        },

        components: {
            myCell,
            headImgField: UploadField,
            evidenceField: UploadField,
        },

        watch:{
            cityPopupVisible(val ){
                if(val) {
                    this.closeTouch()
                } else {
                    this.openTouch()
                }
            },
        },

        computed: {},

        methods: {
            //  点击获取二维码
            getCode() {
                if (this.formData.phonenum) {
                    getInforcode(this.formData.phonenum).then(
                        data => {
                            if (data) {
                                this.useCode();
                                this.$toast('验证码已发送');
                            }
                        }
                    )
                } else {
                    this.$toast('请输入联系电话!');
                }
            },
            // 二维码已发送
            useCode() {
                this.lastEnableCodeSecond = 60;
                this.timer = setInterval(() => {
                    if (this.lastEnableCodeSecond > 0) {
                        this.lastEnableCodeSecond--;
                    } else {
                        if (this.timer) {
                            clearInterval(this.timer)
                        }
                    }
                }, 1000);
            },
            //  显示选择打款方式
            showTransferWay() {
                // setTimeout(() => {
                    this.twSheetVisible = true
                // }, 300)
            },
            //  选择付款方式
            selectTransferWay(evt) {
                this.transferWay = evt.name;
                this.formData.paytype = evt.type;
            },

            openDatePicker(){
                this.closeTouch();

                this.$refs.picker.open();
            },
            //  确定打款日期
            dateTimeConfirm(evt) {
                this.openTouch();

                this.date = evt.toLocaleString('zh-CN', {hour12: false});
            },
            closeDatePicker(){
                this.openTouch();
            },

            showCityPopup() {
                if (!this.allArea.length) {
                    if (getStore(ALL_AREA)) {
                        this.initCityPicker();
                        // setTimeout(() => {
                            this.cityPopupVisible = true
                        // }, 300)
                    } else {
                        getAllArea().then(
                            ({data}) => {
                                setStore(ALL_AREA, data);
                            }
                        )
                    }
                } else {
                    // setTimeout(() => {
                        this.cityPopupVisible = true
                    // }, 300)
                }
            },
            onValuesChange(picker, values) {
                if (!values[0] || !this.allArea.length) {
                    return
                }
                //  数据没拿到
                let pickProvince = this.allArea.find(item => item.id == values[0].id);

                if (pickProvince) {
                    let citys = pickProvince.city.map(item => {
                        return {
                            id: item.id,
                            name: item.name,
                            area: item.area
                        }
                    })
                    picker.setSlotValues(1, citys);

                    if (values[1]) {
                        let pickCity = citys.find(item => item.id == values[1].id);

                        if (pickCity) {
                            picker.setSlotValues(2, pickCity.area)

                            this.pickAreaVal = values;
                        }
                    }
                }
            },
            confirmPickArea() {
                if (this.pickAreaVal[2] && this.pickAreaVal[2].id) {
                    this.formData.cityid = '';

                    this.formData.areaid = this.pickAreaVal[2].id;
                    this.city = this.pickAreaVal[0].name + ' ' + this.pickAreaVal[1].name + ' ' + this.pickAreaVal[2].name;
                    this.cityPopupVisible = false;
                } else if (this.pickAreaVal[1] && this.pickAreaVal[1].id) {
                    this.formData.areaid = '';

                    this.formData.cityid = this.pickAreaVal[1].id;
                    this.city = this.pickAreaVal[0].name + ' ' + this.pickAreaVal[1].name;
                    this.cityPopupVisible = false;
                }

            },
            initCityPicker() {
                this.allArea = JSON.parse(getStore(ALL_AREA));
                this.slots[0].values = this.allArea.map(item => {
                    return {
                        id: item.id,
                        name: item.name,
                    }
                });
                this.slots[2].values = this.allArea[0].city.map(item => {
                    return {
                        id: item.id,
                        name: item.name,
                    }
                });
                this.slots[4].values = this.allArea[0].city[0].area;
            },

            /*解决页面层级相互影响滑动的问题*/
            handler: function(e){
                e.preventDefault()
            },
            closeTouch () {
                document.getElementsByTagName('body')[0].addEventListener('touchmove', this.handler, {passive:false})//阻止默认事件
            },
            openTouch () {
                document.getElementsByTagName('body')[0].removeEventListener('touchmove', this.handler, {passive:false})//打开默认事件
            },

            updateNewHeadImg(imgs) {
                this.headImgs = imgs;
            },
            listenHdUpload(bool) {
                this.isHdImgUploading = bool;
            },

            updateEvdImg(imgs) {
                this.evidenceImgs = imgs;
            },
            listenEvdUpload(bool) {
                this.isEvdImgUploading = bool;
            },

            formDataCheck() {

                if (!this.formData.username) {
                    return '请输入姓名'
                }
                if (!this.formData.phonenum) {
                    return '请输入联系电话'
                }
                if (!this.formData.inforcode) {
                    return '请输入验证码'
                }
                if (!this.formData.password) {
                    return '请输入密码'
                }
                if (!this.passwordConfirm) {
                    return '请再次输入密码'
                }
                if (this.formData.password != this.passwordConfirm) {
                    return '两次密码输入不一致'
                }
                if (!this.formData.idcardnum) {
                    return '请输入身份证号'
                }
                if (!this.formData.wechat) {
                    return '请输入微信号'
                }
                if (!this.formData.cityid && !this.formData.areaid) {
                    return '请选择省市县'
                }
                if (!this.formData.details) {
                    return '请输入详细地址'
                }
                if (this.formData.paytype == 1) {
                    if (!this.formData.alipaynum) {
                        return '请输入支付宝账号'
                    }
                }
                if (this.formData.paytype == 2) {
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
                if (!this.date) {
                    return '请输入打款日期'
                } else {
                    this.formData.paytime = TimeFormater(new Date(this.date)).format('YYYYMMDDHHmmss');
                }

                if (!this.headImgs[0]) {
                    return '请上传头像'
                } else {
                    this.formData.headimg = this.headImgs[0];
                }

                if (!this.headImgs[0]) {
                    return '请上传头像'
                } else {
                    this.formData.headimg = this.headImgs[0];
                }

                if (!this.evidenceImgs[0]) {
                    return '请上传凭证'
                } else {
                    this.formData.proof = this.evidenceImgs.join(',');
                }
            },
            doConfirm() {
                let checkRes = this.formDataCheck();

                if (checkRes) {
                    this.$toast(checkRes);
                } else {
                    this.$messagebox.confirm('确认提交注册表单').then(
                        () => {
                            register(this.formData).then(
                                resData => {
                                    if (resData) {
                                        this.$router.push('/login');
                                        this.$messagebox('您的注册已进入审核状态,我们会尽快处理您的申请,请耐心等待审核!')

                                        // this.$mes('恭喜您成为蓓莉云仓代理的一员!!!');
                                    }
                                }
                            )
                        }
                    )
                }

            },

        },

        destroyed() {
            //  定时器解除
            if (this.timer) {
                clearTimeout(this.timer)
            }
        },

        created() {
            this.formData.qrid = this.$route.query.QRid;

            if (getStore(ALL_AREA)) {
                this.initCityPicker();
            }

            getRegisterInfo(this.$route.query.QRid).then(
                resData => {
                    if (resData) {
                        this.registerInfo = resData.data;

                        this.formData.preusername = this.registerInfo.name;
                        this.formData.prephonenum = this.registerInfo.USphonenum;
                        this.formData.payamount = this.registerInfo.money;
                    }
                }
            )
        },
    }
</script>

