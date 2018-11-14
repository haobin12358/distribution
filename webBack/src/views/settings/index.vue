<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        /*padding: 0 1rem;*/

        .demo-table-expand {
            margin-top: .4rem;
            .el-form-item{

                /*margin-right: 0;*/
                /*margin-bottom: 0;*/
                /*width: 48%;*/
            }
        }

        .confirm-btn-wrap {
            /*padding-right: 25%;*/
            /*float: right;*/
        }
    }
</style>

<template>
    <div class="container">
        <!--<span class="my-title">-->
            <!--LOGO:-->
        <!--</span>-->
        <!--<el-upload-->
            <!--class="avatar-uploader"-->
            <!--:action="$api.uploadFile"-->
            <!--:show-file-list="false"-->
            <!--accept="image/*"-->
            <!--:on-success="handleAvatarSuccess"-->
            <!--:before-upload="beforeAvatarUpload"-->
        <!--&gt;-->
            <!--<img v-if="imageUrl" v-lazy="imageUrl" class="avatar">-->
            <!--<i v-else class="el-icon-plus avatar-uploader-icon"></i>-->

            <!--<div slot="tip" class="el-upload__tip">-->
                <!--建议为方形,大小不要超过10M,上传成功后会显示,上传大图请耐心等待-->
            <!--</div>-->
        <!--</el-upload>-->
        <el-col :span="16">
            <el-form  class="demo-table-expand" size="medium" label-position="right" label-width="100px">

                <el-form-item label="支付宝账户名:">
                    <el-input v-model="formData.alipayname"></el-input>
                </el-form-item>
                <el-form-item label="银行名:">
                    <el-input v-model="formData.bankname"></el-input>
                </el-form-item>

                <el-form-item label="支付宝账号:">
                    <el-input v-model="formData.alipaynum"></el-input>
                </el-form-item>
                <el-form-item label="银行户名:">
                    <el-input v-model="formData.accountname"></el-input>
                </el-form-item>

                <el-form-item label="客服微信:">
                    <el-input v-model="formData.wechat"></el-input>
                </el-form-item>
                <el-form-item label="银行账号:">
                    <el-input v-model="formData.cardnum"></el-input>
                </el-form-item>

                <el-form-item label="注册费:">
                    <el-input v-model="formData.agentmoney" type="number"></el-input>
                </el-form-item>


                <el-form-item label="保证金:">
                    <el-input v-model="formData.bail" type="number"></el-input>
                </el-form-item>

                <el-form-item label="提现指定银行:">
                    <el-input v-model="formData.drawbank"></el-input>
                </el-form-item>
                <el-form-item label="直推奖励:">
                    <el-input v-model="formData.reward" type="number"></el-input>
                </el-form-item>

                <el-form-item>
                    <el-button type="info" @click="setData">重 置</el-button>
                    <el-button type="primary" @click="doConfirm">保 存</el-button>
                </el-form-item>
            </el-form>
        </el-col>

        <!--</el-col>-->
    </div>
</template>

<script>
    export default {
        name: "index",

        data() {
            return {
                imageUrl: '',

                formData: {
                    "alipaynum": "",
                    "alipayname": "",
                    "bankname": "",
                    "accountname": "",
                    "cardnum": "",
                    "agentmoney": 398,
                    "wechat": "",
                    "drawbank": "",
                    "bail": 0,
                    "reward": 100,
                }
            }
        },

        components: {},

        computed: {},

        methods: {
            handleAvatarSuccess(res, file) {
                this.formData.prpic = res.data;
                this.imageUrl = URL.createObjectURL(file.raw);
            },
            beforeAvatarUpload(file) {
                const isLt15M = file.size / 1024 / 1024 < 10;

                if (!isLt15M) {
                    this.$message.error('上传商品图片大小不能超过 10MB!');
                }

                if (isLt15M) {
                    this.imageUrl = '';
                    this.clearUploadedImg();
                }

                return isLt15M;
            },

            setData(){
                this.$http.get(this.$api.getConfigure,{
                    params: {
                        token: this.$common.getStore('token')

                    }
                }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.formData = data;
                        }
                    }
                )
            },

            doConfirm(){
                this.$confirm(`确定保存平台配置?`, '提示', {
                    type: 'info'
                }).then(
                    ()=>{
                        this.$http.post(this.$api.updateAccounts,
                            this.formData
                        ,{
                            params: {
                                token: this.$common.getStore('token')

                            }
                        }).then(
                            res => {
                                if (res.data.status == 200) {
                                    let resData = res.data,
                                        data = res.data.data;

                                    this.setData();
                                    this.$notify({
                                        title: '平台配置保存成功',
                                        type: 'success'
                                    });
                                }
                            }
                        )
                    }
                )
            }
        },

        created() {
this.setData();
        },
    }
</script>

