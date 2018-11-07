<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .line {
            text-align: center;
            .fz(.3rem);
            font-weight: bold;
        }

        .avatar-uploader .el-upload {
            border: 1px dashed #d9d9d9;
            border-radius: 6px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        .avatar-uploader .el-upload:hover {
            border-color: #409EFF;
        }
        .avatar-uploader-icon {
            font-size: 28px;
            color: #8c939d;
            width: 178px;
            height: 178px;
            line-height: 178px;
            text-align: center;
        }
        .avatar {
            width: 178px;
            height: 178px;
            display: block;
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
                <el-form :model="formData" label-position="left" ref="ruleForm" size="medium" label-width="100px"
                         class="demo-ruleForm">
                    <el-form-item label="商品名" >
                        <el-input v-model.trim="formData.PRname"></el-input>
                    </el-form-item>
                    <el-form-item label="商品图片">
                        <!--<el-upload-->
                            <!--class="swiper-uploader"-->
                            <!--action="https://jsonplaceholder.typicode.com/posts/"-->
                            <!--list-type="picture-card"-->
                            <!--:on-preview="handlePictureCardPreview"-->
                            <!--:on-remove="handleRemove"-->
                            <!--:limit="1">-->
                            <!--<i class="el-icon-plus"></i>-->
                        <!--</el-upload>-->
                        <el-upload
                            class="avatar-uploader"
                            :action="$api.uploadFile"
                            :show-file-list="false"
                            :on-success="handleAvatarSuccess"
                            :before-upload="beforeAvatarUpload"
                            :on-preview="handlePictureCardPreview"
                            :on-remove="handleRemove"
                        >
                            <img v-if="imageUrl" :src="imageUrl" class="avatar">
                            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                        </el-upload>
                    </el-form-item>
                    <el-form-item label="分类" >
                        <el-cascader :options="options" v-model="selectedOption">
                        </el-cascader>
                    </el-form-item>
                    <el-form-item label="原价格" >
                        <el-input v-model="formData.PRoldprice" type="number"></el-input>
                    </el-form-item>
                    <el-form-item label="价格">
                        <el-input v-model="formData.PRprice" type="number"></el-input>
                    </el-form-item>
                    <el-form-item label="库存" >
                        <el-input v-model="formData.PRstock" type="number"></el-input>
                    </el-form-item>
                    <el-form-item label="邮费" >
                        <el-input v-model="formData.PRlogisticsfee" type="number"></el-input>
                    </el-form-item>
                    <el-form-item label="返点件数" >
                        <el-input v-model="formData.PAdiscountnum" type="number"></el-input>
                    </el-form-item>

                    <el-form-item>
                        <el-button type="primary">立即创建</el-button>
                        <el-button>重置</el-button>
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
    export default {
        name: "productEdit",

        data() {
            return {
                dialogImageUrl: '',
                dialogVisible: false,

                imageUrl: '',


                options: [
                    {
                        value: '0-1',
                        label: '上衣',
                        children: [{
                            value: '1-1',
                            label: '短袖',
                        }, {
                            value: '1-2',
                            label: '卫衣',
                        }, {
                            value: '1-3',
                            label: '衬衫',
                        },]
                    },{
                        value: '0-2',
                        label: '下装',
                        children: [{
                            value: '1-1',
                            label: '短裤',
                        }, {
                            value: '1-2',
                            label: '长裤',
                        }, ]
                    },
                ],
                selectedOption: [],

                formData: {
                    PRname: '',
                    PRoldprice: '',
                    PRprice: '',
                    PRlogisticsfee: '',
                    PAdiscountnum: '',
                    PRstock: '',

                },
                // rules: { todo 校验
                //     name: [
                //         { required: true, message: '请输入活动名称', trigger: 'blur' },
                //         { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
                //     ],
                //     region: [
                //         { required: true, message: '请选择活动区域', trigger: 'change' }
                //     ],
                //     date1: [
                //         { type: 'date', required: true, message: '请选择日期', trigger: 'change' }
                //     ],
                //     date2: [
                //         { type: 'date', required: true, message: '请选择时间', trigger: 'change' }
                //     ],
                //     type: [
                //         { type: 'array', required: true, message: '请至少选择一个活动性质', trigger: 'change' }
                //     ],
                //     resource: [
                //         { required: true, message: '请选择活动资源', trigger: 'change' }
                //     ],
                //     desc: [
                //         { required: true, message: '请填写活动形式', trigger: 'blur' }
                //     ]
                // }
            }
        },

        components: {},

        computed: {},

        methods: {
            handleRemove(file, fileList) {
                console.log(file, fileList);
            },
            handlePictureCardPreview(file) {
                this.dialogImageUrl = file.url;
                this.dialogVisible = true;
            },

            handleAvatarSuccess(res, file) {
                this.imageUrl = URL.createObjectURL(file.raw);
            },
            beforeAvatarUpload(file) {
                const isJPG = file.type === 'image/jpeg';
                const isLt2M = file.size / 1024 / 1024 < 2;

                if (!isJPG) {
                    this.$message.error('上传头像图片只能是 JPG 格式!');
                }
                if (!isLt2M) {
                    this.$message.error('上传头像图片大小不能超过 2MB!');
                }
                return isJPG && isLt2M;
            }
        },

        created() {
        },
    }
</script>

