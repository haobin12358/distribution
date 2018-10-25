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
        input:focus{
            background: yellow;
        }
        .main-form {


        }

        .city-picker-popup{
            width: 100%;

            .city-picker-toolbar{
                .fj();
                padding: 10px  30px;

                button{
                    .bgw();
                    .sc(38px, #26b83a);

                    &.cancel-btn{
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
            <my-cell title="邀请代理" value="xx" :readonly="true"></my-cell>
            <my-cell title="联系电话" value="12366666666" :readonly="true"></my-cell>
            <my-cell title="联系地址" value="浙江省杭州市江干区九环路九润公寓浙江省杭州市江干区九环路九润公寓" :readonly="true"></my-cell>
        </section>

        <section class="form-title">
            填写内容
        </section>

        <section class="main-form">
            <mt-field label="姓名" placeholder="请输入姓名"></mt-field>
            <mt-field label="联系电话" placeholder="请输入联系电话"></mt-field>
            <mt-field label="验证码" placeholder="请输入验证码"></mt-field>
            <mt-field label="密码" placeholder="请输入登录密码"></mt-field>
            <mt-field label="密码确认" placeholder="请再次输入登录密码"></mt-field>
            <mt-field label="微信号" placeholder="请输入微信号"></mt-field>
            <mt-field label="身份证号" placeholder="请输入身份证号"></mt-field>
            <mt-field label="国家地区" placeholder="请选择国家地区" v-model="city" :readonly="true"
                      :disableClear="true" @click.native="showCityPopup"></mt-field>
            <mt-field class="form-item" label="省市县" placeholder="请选择省市县" v-model="city" :readonly="true"
                      :disableClear="true" @click.native="showCityPopup"></mt-field>

            <mt-field class="form-item" label="打款方式" placeholder="请选择打款方式" v-model="transferWay" :readonly="true"
                      :disableClear="true" @click.native="showTransferWay"></mt-field>
            <mt-field class="form-item" label="支付宝" placeholder="请输入支付宝账号"></mt-field>
            <mt-field class="form-item" label="金额" placeholder="请输入打款金额" type="number"></mt-field>
            <mt-field class="form-item" label="打款日期" placeholder="请输入打款日期" :readonly="true" :disableClear="true"
                      v-model="date" @click.native="$refs.picker.open()"></mt-field>
            <head-img-field label="头像"></head-img-field>
            <upload-field label="头像"></upload-field>
            <evidence-field label="打款凭证(1-2张)"></evidence-field>
        </section>

        <section class="form-title">
            请打款至
        </section>


        <section class="inviter-info">
            <my-cell title="支付宝账号" value="zhelishiwoluanxiede@163.com" :readonly="true"></my-cell>
            <my-cell title="支付宝实名" value="某某" :readonly="true"></my-cell>
            <my-cell title="客服微信" value="beiliyuncang123" :readonly="true"></my-cell>
        </section>

        <section class="my-confirm-btn-wrap" style="margin: 30px 0 60px;">
            <button class="my-confirm-btn">确 认</button>
        </section>

        <mt-popup class="city-picker-popup" position="bottom" v-model="cityPopupVisible">
            <mt-picker :slots="slots" @change="onValuesChange" :showToolbar="true">
                <section class="city-picker-toolbar">
                    <button class="cancel-btn">取消</button>
                    <button>确认</button>
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
            v-model="datetime"
            @confirm="dateTimeConfirm"
        >
        </mt-datetime-picker>
    </div>
</template>

<script>
    import myCell from "src/components/common/myCell"
    import uploadField from "src/components/common/uploadField"

    export default {
        name: "applyAgent",

        data() {
            return {
                city: '',
                transferWay: '',
                birthday: '',
                date: '',

                cityPopupVisible: false,
                slots: [
                    {
                        flex: 1,
                        values: ['浙江省'],
                        className: 'slot1',
                        textAlign: 'right'
                    }, {
                        divider: true,
                        content: '-',
                        className: 'slot2'
                    }, {
                        flex: 1,
                        values: ['杭州市','宁波市','温州市'],
                        className: 'slot3',
                        textAlign: 'left'
                    } ,{
                        divider: true,
                        content: '-',
                        className: 'slot4'
                    }, {
                        flex: 1,
                        values: ['西湖区','滨江区','萧山区'],
                        className: 'slot5',
                        textAlign: 'left'
                    }
                ],

                transferWayActions: [
                    {name: '支付宝', method: this.selectTransferWay},
                    {name: '微信', method: this.selectTransferWay},
                    {name: '银行卡', method: this.selectTransferWay},
                ],
                twSheetVisible: false,


                datetime: ''
            }
        },

        components: {
            myCell,
            headImgField: uploadField,
            evidenceField: uploadField,
        },

        computed: {},

        methods: {
            selectTransferWay(evt) {
                this.transferWay = evt.name;
            },
            dateTimeConfirm(evt) {
                this.date = evt.toLocaleString('zh-CN', {hour12: false});
            },
            onValuesChange(picker, values) {

            },
            showCityPopup(){
                setTimeout(()=>{
                    this.cityPopupVisible = true
                }, 300)
            },
            showTransferWay(){
                setTimeout(()=>{
                    this.twSheetVisible = true
                }, 300)
            },
        },

        created() {
        },
    }
</script>

