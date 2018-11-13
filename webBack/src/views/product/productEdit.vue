<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .line {
            text-align: center;
            .fz(.3rem);
            font-weight: bold;
        }


    }
</style>

<template>
    <div class="container">
        <el-breadcrumb style="margin-bottom: .2rem;" separator-class="el-icon-arrow-right">
            <el-breadcrumb-item to="index">所有商品</el-breadcrumb-item>
            <el-breadcrumb-item>商品编辑</el-breadcrumb-item>
        </el-breadcrumb>


        <el-row style="margin-top: .3rem;">
            <el-col :span="14">
                <el-form :model="formData" :rules="rules" label-position="left" ref="ruleForm" size="medium"
                         label-width="100px"
                         class="demo-ruleForm">
                    <el-form-item prop="prname" label="商品名">
                        <el-input v-model.trim="formData.prname"></el-input>
                    </el-form-item>
                    <el-form-item prop="prpic" label="商品图片(限一张)">
                        <el-upload
                            class="avatar-uploader"
                            :action="$api.uploadFile"
                            :show-file-list="false"
                            accept="image/*"
                            :on-success="handleAvatarSuccess"
                            :before-upload="beforeAvatarUpload"
                        >
                            <img v-if="imageUrl"  v-lazy="imageUrl" class="avatar">
                            <i v-else class="el-icon-plus avatar-uploader-icon"></i>

                            <div slot="tip" class="el-upload__tip">
                                建议为方形,大小不要超过10M,上传成功后会显示,上传大图请耐心等待
                            </div>
                        </el-upload>
                    </el-form-item>
                    <el-form-item prop="selectedOption" label="分类">
                        <el-cascader :options="options" :props="cascaderProps" v-model="selectedOption">
                        </el-cascader>
                    </el-form-item>
                    <el-form-item prop="proldprice" label="原价格">
                        <el-input v-model="formData.proldprice" type="number"></el-input>
                    </el-form-item>
                    <el-form-item prop="prprice" label="价格">
                        <el-input v-model="formData.prprice" type="number"></el-input>
                    </el-form-item>
                    <el-form-item prop="prstock" label="库存">
                        <el-input v-model="formData.prstock" type="number"></el-input>
                    </el-form-item>
                    <el-form-item prop="prlogisticsfee" label="邮费(1件时生效)">
                        <el-input v-model="formData.prlogisticsfee" type="number"></el-input>
                    </el-form-item>
                    <el-form-item prop="padiscountnum" label="返点件数">
                        <el-input v-model="formData.prdiscountnum" type="number"></el-input>
                    </el-form-item>

                    <el-form-item>
                        <el-button type="primary" @click="doSavePd">{{isEdit ? '保存' : '新增'}}</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>

        <el-dialog :visible.sync="dialogVisible">
            <img width="100%" :src="dialogImageUrl" alt="">
        </el-dialog>
    </div>
</template>

<script>
    import lrz from "lrz"

    export default {
        name: "productEdit",

        data() {
            return {
                isEdit: false,

                dialogImageUrl: '',
                dialogVisible: false,

                imageUrl: '',
                keepImg: false,


                options: [],
                cascaderProps: {
                    value: 'PAid',
                    label: 'PAname',
                    children: 'child_category',
                },
                selectedOption: [],

                formData: {
                    prid: "",
                    paid: "",
                    prname: "",
                    prpic: "",
                    proldprice: "",
                    prprice: "",
                    prstock: "",
                    prlogisticsfee: "0",
                    prdiscountnum: "1",
                    prstatus: '1'
                },
                rules: {
                    required: [
                        {required: true, message: '必填', trigger: 'blur'}
                    ],
                    prname: [
                        {required: true, message: '商品名必填', trigger: 'blur'}
                    ],
                    prpic: [
                        {required: true, message: '商品图必传', trigger: 'change'}
                    ],

                    proldprice: [
                        {required: true, message: '原价必填', trigger: 'blur'}
                    ],
                    prprice: [
                        {required: true, message: '折扣价必填', trigger: 'blur'}
                    ],
                    prlogisticsfee: [
                        {required: true, message: '运费必填(可为0)', trigger: 'blur'}
                    ],
                    prdiscountnum: [
                        {required: true, message: '返点件数必填', trigger: 'blur'}
                    ],
                    prstock: [
                        {required: true, message: '库存必填', trigger: 'blur'}
                    ],
                },
            }
        },

        components: {},

        computed: {},

        methods: {
            handleRemove(file, fileList) {
                this.imageUrl = '';
                this.formData.prpic = '';
            },
            handlePictureCardPreview(file) {
                this.dialogImageUrl = file.url;
                this.dialogVisible = true;
            },
            handleAvatarChange(file, fileList){
                // console.log('[change]', file, fileList);
            },
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

            clearUploadedImg(){
                  if(this.formData.prpic){
                      this.$http.post(this.$api.removeFile, {
                          url: this.formData.prpic.split('file/')[1]
                      }, {
                          noLoading: true,
                          params: {
                              token: this.$common.getStore('token')
                          }
                      }).then()
                  }
            },

            setCategoryList() {
                this.$http.get(this.$api.getProductCategoryList).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.options = data;
                        }
                    }
                )
            },

            doSavePd() {
                this.formData.paid = this.selectedOption[1];

                this.$http.post(this.$api.saveProduct, this.formData,{
                    params: {
                        token: this.$common.getStore('token')
                    }
                }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            // this.keepImg = true;
                            this.$router.back();
                            this.$notify({
                                title: '商品保存成功',
                                message: `商品名:${this.formData.prname}`,
                                type: 'success'
                            });
                        }
                    }
                )
            },
        },

        destroyed(){
            // this.clearUploadedImg();
        },

        created() {
            this.setCategoryList();

            let editPd = this.$route.query.pd;

            if (editPd) {
                this.isEdit = true;

                this.formData.prid = editPd.PRid;
                this.formData.paid = editPd.PAid;
                this.formData.prname = editPd.PRname;
                this.formData.prpic= editPd.PRpic;
                this.formData.proldprice = editPd.PRoldprice;
                this.formData.prprice = editPd.PRprice;
                this.formData.prstock = editPd.PRstock;
                this.formData.prlogisticsfee= editPd.PRlogisticsfee;
                this.formData.prdiscountnum= editPd.PAdiscountnum;
                this.formData.prstatus = editPd.PRstatus;;

                this.imageUrl = editPd.PRpic;


                this.selectedOption =  [editPd.firstpaid.toString(),editPd.PAid.toString()];
            }

        },
    }
</script>

