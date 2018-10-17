<style lang="less" scoped>
    @import "~src/common/css/index";

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
        }
    }
</style>

<template>
    <div class="forget-password">
        <header-top :title="'修改密码'" showBack="true"></header-top>
        <form class="forget-password-form" v-on:submit.prevent>
            <div class="form-item">
                <section class="form-item-label">
                    <span class="label__start"></span>
                    <span class="label__text">联系电话</span>

                </section>

                <input type="text" class="form-item-input" placeholder="请输入联系电话">
            </div>

            <div class="form-item">
                <section class="form-item-label">
                    <span class="label__start"></span>
                    <span class="label__text">验证码</span>
                </section>
                <!--<div class="form-item-input">请输入验证码</div>-->
                <input type="text" class="form-item-input" style="width: 100px;" placeholder="请输入验证码">
                <button class="form-item-code">获取</button>
            </div>

            <div class="form-item">
                <section class="form-item-label">
                    <span class="label__start"></span>
                    <span class="label__text">新密码</span>

                </section>

                <input type="text" class="form-item-input" placeholder="请输入登录密码">

            </div>

            <div class="form-item">
                <section class="form-item-label">
                    <span class="label__start"></span>
                    <span class="label__text">密码确认</span>

                </section>

                <input type="text" class="form-item-input" placeholder="请再次输入登录密码">
            </div>
        </form>

        <button class="confirm-btn">确 定</button>
    </div>
</template>

<script>

    export default {
        name: "forgetPassword",

        data() {
            return {}
        },

        components: {
        },

        methods: {},
    }
</script>

