<style lang="less" scoped>
    @import "../../../common/css/index";

    .forget-password {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: @bgMainColor;
        z-index: 10;

        .forget-password-form {
            padding: 66px 74px 81px 51px;
            box-shadow: 0px 5px 5px rgba(0, 0, 0, 0.16);
            background-color: white;
            margin-top: 20px;

            .form-item {
                padding-bottom: 37px;
                border-bottom: 1px solid #CCCCCC;
                margin-bottom: 37px;
                .fj();
                align-items: flex-end;
                .fz(26px);

                .form-item-label {

                    width: 140px;
                    margin-right: 50px;
                    .fj(flex-start);
                    align-items: flex-end;

                    .label__start {
                        display: inline-block;
                        width: 5px;
                        height: 50px;
                        line-height: 50px;
                        background: @mainLightColor;
                        margin-right: 16px;
                    }
                }

                .form-item-input {
                    .fz(26px);
                    flex: 1;
                }

                .form-item-code {
                    width: 157px;
                    height: 40px;
                    border: 1px solid @mainColor;
                    border-radius: 30px;
                    .fontc(40px);
                    .fz(24px);
                    background: white;
                }
            }
        }

        .confirm-btn {
            .wl(364px, 90px);
            background: linear-gradient(180deg, @mainLightColor 0%, @mainColor 100%);
            .sc(38px, white);
            .fontc(90px);
            font-weight: bold;
            border-radius: 50px;
            margin-top: 285px;
            border: none;
        }
    }
</style>

<template>
    <div class="forget-password">
        <header-top :title="'修改密码'" :showBack="true"></header-top>
        <form class="forget-password-form" v-on:submit.prevent>
            <div class="form-item">
                <section class="form-item-label">
                    <span class="label__start"></span>
                    <span class="label__text">联系电话</span>

                </section>

                <input type="tel" v-model.trim="tel" class="form-item-input" placeholder="请输入联系电话">
            </div>

            <div class="form-item">
                <section class="form-item-label">
                    <span class="label__start"></span>
                    <span class="label__text">验证码</span>
                </section>
                <!--<div class="form-item-input">请输入验证码</div>-->
                <input type="text" v-model.trim="code" class="form-item-input" style="width: 100px;"
                       placeholder="请输入验证码">
                <!--<button class="form-item-code" :disabled="codeDisabledTime" @click="getCode">{{codeDisabledTime ?-->
                <!--`剩余${codeDisabledTime}s` :'获取'}}-->
                <!--</button>-->
                <button class="form-item-code" :disabled="lastEnableCodeSecond>0" @click="getCode">
                    {{lastEnableCodeSecond>0 ?`剩余${lastEnableCodeSecond}s`: '获取'}}
                </button>
            </div>

            <div class="form-item">
                <section class="form-item-label">
                    <span class="label__start"></span>
                    <span class="label__text">新密码</span>

                </section>

                <input type="password" v-model="newPassword" class="form-item-input" placeholder="请输入登录密码">
            </div>

            <div class="form-item">
                <section class="form-item-label">
                    <span class="label__start"></span>
                    <span class="label__text">密码确认</span>
                </section>

                <input type="password" v-model="newPasswordConfirm" class="form-item-input" placeholder="请再次输入登录密码">
            </div>
        </form>

        <button class="confirm-btn" @click="confirmUpdate">确 定</button>
    </div>
</template>

<script>
    import {getInforcode, findBackPwd} from "src/api/api"
    import {setStore, getStore} from "src/common/js/mUtils"
    import {TOKEN} from "src/common/js/const"

    export default {
        name: "forgetPassword",

        data() {
            return {
                tel: '',
                code: '',
                newPassword: '',
                newPasswordConfirm: '',

                timer: null,
                lastEnableCodeSecond: 0,    //  下一次可用验证码倒计时
            }
        },

        computed: {},

        components: {},

        methods: {
            useCode() {
                this.lastEnableCodeSecond = 60;
                this.timer = setInterval(() => {
                    if (this.lastEnableCodeSecond > 0)
                        this.lastEnableCodeSecond--;
                }, 1000);
            },
            getCode() {
                if (this.tel) {

                    getInforcode(this.tel).then(
                        data => {
                            if (data) {
                                this.useCode();
                                this.$toast('验证码已发送');
                            }
                        }
                    )
                } else {
                    this.$toast('请输入手机号!');
                }
            },

            formDataCheck() {
                let checkRes = '';

                if (!this.tel) {
                    return '请填写手机号!';
                }
                if (!this.code) {
                    return '请填写验证码!';
                }
                if (!this.newPassword) {
                    return '请填写新密码!';
                }
                if (!this.newPasswordConfirm) {
                    return '请填写新密码确认!';
                }

                if (this.newPassword != this.newPasswordConfirm) {
                    return '两次密码输入不一致!';
                }
            },

            confirmUpdate() {
                let checkMessage = this.formDataCheck();

                if (!checkMessage) {
                    findBackPwd(this.tel, this.code, this.newPassword).then(
                        data => {
                            if (data) {
                                this.$toast('密码修改成功');
                                this.$router.push('/message')
                            }
                        }
                    )

                } else {
                    this.$toast(checkMessage);
                }
            }
        },

        destroyed(){
            //  定时器解除
            if(this.timer){
                clearTimeout(this.timer)
            }
        },

        created() {
            if (getStore(TOKEN)) {
                this.$router.push('/message');
            }
        }
    }
</script>

