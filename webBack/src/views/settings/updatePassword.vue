<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
    }
</style>

<template>
    <div class="container">
        <el-col :span="16">
            <el-form ref="form" :model="form">

                <el-form-item label="旧密码">
                    <el-input v-model="form.oldpassword" :type="inputType"></el-input>
                </el-form-item>
                <el-form-item label="新密码">
                    <el-input v-model="form.newpassword" :type="inputType"></el-input>
                </el-form-item>
                <el-form-item label="新密码确认">
                    <el-input v-model="form.newpasswordConfirm" :type="inputType"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-switch v-model="showPwd" active-text="显示" inactive-text="隐藏" active-color="#13ce66"
                               inactive-color="#ff4949">
                    </el-switch>
                </el-form-item>

                <el-form-item style="float: right">
                    <el-button type="primary" @click="doConfirm">
                        保 存
                    </el-button>
                </el-form-item>

            </el-form>
        </el-col>
    </div>
</template>

<script>
    export default {
        name: "updatePassword",

        data() {
            return {
                showPwd: false,
                form: {
                    oldpassword: '',
                    newpassword: '',
                    newpasswordConfirm: '',
                }
            }
        },

        components: {},

        computed: {
            inputType() {
                return this.showPwd ? 'text' : 'password';
            },


        },

        methods: {
            formDataCheck() {
                if (!this.form.oldpassword || !this.form.newpassword || !this.form.newpasswordConfirm) {
                    return '请填写完整!'
                }

                if (this.form.newpassword != this.form.newpasswordConfirm) {
                    return '新密码确认不一致!'
                }

            },

            doConfirm() {
                let checkRst = this.formDataCheck();

                if (checkRst) {
                    this.$message.warning(checkRst);
                } else {
                    this.$http.post(this.$api.updatePwd, {
                        "oldpassword": this.form.oldpassword,
                        "newpassword": this.form.newpassword
                    }, {
                        params: {
                            token: this.$common.getStore('token')
                        }
                    }).then(
                        res => {
                            if (res.data.status == 200) {
                                let resData = res.data,
                                    data = res.data.data;

                                this.$notify({
                                    title: '密码修改成功',
                                    message: `请重新登录`,
                                    type: 'success'
                                });

                                this.$common.setStore('token', '');
                                this.$router.push('/login');
                            }
                        }
                    )
                }
            }
        },

        created() {
        },
    }
</script>

