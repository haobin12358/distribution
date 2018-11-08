<template>
    <div class="login-status">
        <div class="login-content">
            <div class="login-box">
                <el-form :model="ruleForm" :rules="rules" ref="ruleForm">
                    <div class="login-head">
                        <h3>蓓莉云仓管理系统</h3>
                    </div>

                    <el-form-item prop="MAname" label="账号">
                        <el-input v-model="ruleForm.MAname" placeholder="输入账号" class="m-input"></el-input>
                    </el-form-item>
                    <el-form-item prop="MApassword" label="密码">
                        <el-input v-model="ruleForm.MApassword" @keyup.enter.native="submitForm('ruleForm')"
                                  placeholder="输入密码" type="password" class="m-input"></el-input>
                    </el-form-item>

                    <el-form-item class="m-btn">
                        <el-button type="primary" @click="submitForm('ruleForm')">登 &nbsp;&nbsp;录</el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-checkbox name="type" v-model="ruleForm.checked">记住密码</el-checkbox>
                    </el-form-item>
                </el-form>
            </div>
        </div>

        <!--<foot></foot>-->
    </div>

</template>

<script>
    import api from '../../api/api';
    import {MessageBox} from 'element-ui';
    import axios from 'axios';

    export default {
        data() {
            return {
                ruleForm: {
                    MAname: '',
                    MApassword: '',
                    checked: true,
                },
                rules: {
                    MAname: [
                        {required: true, message: '请输入账号名称', trigger: 'blur'}
                    ],
                    MApassword: [
                        {required: true, message: '请输入密码', trigger: 'blur'}
                    ],
                }
            };
        },
        //页面加载调用获取cookie值
        mounted() {
            this.getCookie();
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        //记住密码
                        //判断复选框是否被勾选 勾选则调用配置cookie方法
                        if (this.ruleForm.checked == true) {
                            //传入账号名，密码，和保存天数3个参数
                            this.setCookie(this.ruleForm.MAname, this.ruleForm.MApassword, 7);
                        } else {
                            console.log("清空Cookie");
                            //清空Cookie
                            this.clearCookie();
                        }
                        this.$http.post(this.$api.login, {
                            adnum: this.ruleForm.MAname,
                            adpassword: this.ruleForm.MApassword,
                        }).then(
                            res => {
                                if(res.data.status == 200){
                                    this.$common.setStore('token', res.data.data.token);
                                    this.$router.push('/profile');
                                }
                            }
                        )
                    } else {
                        return false;
                    }
                });
            },
            //设置cookie
            setCookie(c_name, c_pwd, exdays) {
                let exdate = new Date(); //获取时间
                exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * exdays); //保存的天数
                //字符串拼接cookie
                window.document.cookie = "userName" + "=" + c_name + ";path=/;expires=" + exdate.toGMTString();
                window.document.cookie = "userPwd" + "=" + c_pwd + ";path=/;expires=" + exdate.toGMTString();
            },
            //读取cookie
            getCookie: function () {
                if (document.cookie.length > 0) {
                    let arr = document.cookie.split('; '); //这里显示的格式需要切割一下自己可输出看下
                    for (let i = 0; i < arr.length; i++) {
                        let arr2 = arr[i].split('='); //再次切割
                        //判断查找相对应的值
                        if (arr2[0] == 'userName') {
                            this.ruleForm.MAname = arr2[1]; //保存到保存数据的地方
                        } else if (arr2[0] == 'userPwd') {
                            this.ruleForm.MApassword = arr2[1];
                        }
                    }
                }
            },
            //清除cookie
            clearCookie: function () {
                this.setCookie("", "", -1); //修改2值都为空，天数为负1天就好了
            },
            forgetPwd() {
                this.$router.push('/forgetPwd');
            }
        },

        created(){
            if(this.$common.getStore('token')){
                this.$router.push('/profile');
            }
        }
    }
</script>

<style lang="less" rel="stylesheet/less" scoped>
    @import "../../common/css/_variate";

    .login-status {
        height: 100%;
        .login-content {
            position: fixed;
            background: url("../../common/images/login-back.png");
            background-size: 100% 100%;
            width: 100%;
            height: 100%;
            .login-box {
                width: 3.6rem;
                /*height: 4.6rem;*/
                padding: 0.6rem;
                position: absolute;
                top: 35%;
                right: 1.2rem;
                background-color: #fff;
                -webkit-transform: translate(0, -1.6rem);
                transform: translate(0, -1.6rem);
                /*border-radius: 5px;*/
                .login-head {
                    margin-bottom: 0.4rem;
                    font-size: 0.25rem;
                    line-height: 0.4rem;
                    color: @mainFont;
                    p {
                        font-size: 0.20rem;
                    }
                }
                .el-form-item {
                    vertical-align: middle;
                    position: relative;
                    /*height: 0.4rem;*/
                    .icon {
                        width: 0.25rem;
                        height: 0.25rem;
                        position: absolute;
                        display: inline-block;
                        top: 0.145rem;
                        left: 0.2rem;
                        z-index: 100;
                    }
                    .icon-person {
                        /*background: url("../../common/images/person.png");*/
                        background-size: 100% 100%;
                    }
                    .icon-r {
                        width: 0.2rem;
                        height: 0.2rem;
                        position: absolute;
                        display: inline-block;
                        top: 0.185rem;
                        right: 0.1rem;
                        z-index: 100;
                    }
                    .icon-pwd {
                        /*background: url("../../common/images/pwd.png") no-repeat ;*/
                        background-size: 100% 100%;
                    }
                    button {
                        width: 3.6rem;
                        height: 0.54rem;
                        text-align: center;
                        font-size: 0.2rem;
                        background-color: @btnActiveColor;
                        border-color: @btnActiveColor;
                        margin-top: 0.2rem;
                        border-radius: 0;
                    }
                    .m-forget-pwd {
                        color: @greyColor;
                        /*display: inline-block;*/
                        position: absolute;
                        top: 0;
                        right: 0;
                        cursor: pointer;
                    }
                }
            }
        }

    }


</style>
