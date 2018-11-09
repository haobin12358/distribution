<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        background: url("/static/images/testbg.jpg");
        background-size: cover;
        width: 100%;
        min-height: 100vh;
        overflow: hidden;
        /*position: fixed;*/

        .fj(flex-start);
        .fcolum();
        text-align: center;

        .container-hd {
            .sc(38px, @mainColor);
            font-weight: bold;
            margin: 69px 0 18px;
        }

        .container-bd {
            .wl(615px, 816px);
            border-radius: 30px;
            padding: 75px 69px 16px;
            box-sizing: border-box;
            background: white;
            .fj(flex-start);
            .fcolum();

            .platform-logo {
                .wl(234px, 234px);
                border: 10px solid #707070;
                box-sizing: border-box;
                border-radius: 50%;
                margin-bottom: 131px;
                box-shadow: 0px 10px 3px rgba(0, 0, 0, 0.16);
            }

            .login-input {
                width: 490px;
                height: 70px;
                border: 1px solid @mainColor;
                box-shadow: -5px 5px 0px rgba(0, 0, 0, 0.16);
                opacity: 0.5;
                border-radius: 50px;
                margin-bottom: 70px;
                padding-left: 38px;
                .fz(24px);

                &:last-child {
                    margin-bottom: 118px;
                }
            }

            .forget-pwd {
                color: @mainFontColor;
                font-size: 24px;
                text-align: right;
                align-self: flex-end;
            }

        }

        .container-ft {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            margin-top: 50px;

            .confirm-btn {
                .wl(364px, 90px);
                background: linear-gradient(180deg, @mainLightColor 0%, @mainColor 100%);
                .sc(38px, white);
                .fontc(90px);
                font-weight: bold;
                border-radius: 50px;
                border: none;

            }
        }
    }
</style>

<template>
    <div class="container">
        <header class="container-hd">
            会员登录平台
        </header>
        <section class="container-bd">
            <img class="platform-logo" src="/static/images/testbg.jpg" alt="">

            <input type="tel" v-model.trim="username" class="login-input" placeholder="请输入手机号码">
            <input type="password" v-model="password" class="login-input" placeholder="请输入密码">
            <!--<mt-field  placeholder="请输入手机号码"></mt-field>-->
            <!--<mt-field  placeholder="请输入密码"></mt-field>-->


            <span class="forget-pwd" @click="gotoForgetPassword">忘了密码？</span>
        </section>
        <footer class="container-ft">
            <button class="confirm-btn" @click="doLogin">登 录</button>
        </footer>

        <transition name="router-slid" mode="out-in">
            <router-view></router-view>
        </transition>
    </div>
</template>

<script>
    import {login,getCompanyMessage} from "src/api/api"
    import {setStore, getStore} from "src/common/js/mUtils"
    import {TOKEN,NOT_READ_COM_MSGS} from "src/common/js/const"
    import {mapActions} from "vuex"


    export default {
        name: "login",

        data() {
            return {
                username: '',
                password: '',
            }
        },

        components: {},

        methods: {
            ...mapActions(['getUserInfo','setNotReadMsgNum']),
            gotoForgetPassword() {
                this.$router.push('/login/forgetPassword');
            },
            doLogin() {
                if (this.username && this.password) {
                    login(this.username, this.password).then(
                        data => {
                            if (data) {
                                setStore(TOKEN, data.data.token);
                                this.$toast('登录成功');
                                this.$router.push('/mall');
                                this.setNotReadMsgNum();
                                this.getUserInfo();

                                this.$http.get(title+'/user/check_openid',{
                                    params: {
                                        token: getStore(TOKEN),
                                        state: location.href,
                                    }
                                }).then(
                                    res => {
                                        if (res.data.status == 302) {
                                            let resData = res.data,
                                                data = res.data.data;

                                            location.href = data.url;
                                        }
                                    }
                                )
                            }
                        }
                    )
                } else {
                    this.$toast('请填写完整!');
                }
            },

        },

        created() {
            if (getStore(TOKEN)) {
                this.setNotReadMsgNum();
                this.$router.push('/mall');
                this.$toast('已登录');
            }
        }
    }
</script>

