<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .swiper-uploader {
            .el-upload {
                .wl(4.7rem, 1.1rem);
            }
        }
    }
</style>

<template>
    <div class="container">
        <el-breadcrumb style="margin-bottom: .2rem;" separator="/">
            <el-breadcrumb-item>轮播图管理</el-breadcrumb-item>
        </el-breadcrumb>

        <section class="swiper-section">
            <header class="my-title fcm">
                云仓轮播图
            </header>

            <el-upload
                class="swiper-uploader"
                action="https://jsonplaceholder.typicode.com/posts/"
                list-type="picture-card"
                :file-list="mallImgList"
                :on-preview="handlePictureCardPreview"
                :on-remove="handleRemove"
                :limit="1">
                <i class="el-icon-plus"></i>
            </el-upload>
            <el-dialog :visible.sync="dialogVisible">
                <img width="100%" :src="dialogImageUrl" alt="">
            </el-dialog>
        </section>

        <section class="swiper-section">
            <header class="my-title fcm">
                我的轮播图
            </header>

            <el-upload
                class="avatar-uploader"
                action="https://jsonplaceholder.typicode.com/posts/"
                list-type="picture-card"
                :file-list="personImgList"
                :on-preview="handlePictureCardPreview"
                :on-remove="handleRemove">
                <i class="el-icon-plus"></i>
            </el-upload>
            <el-dialog :visible.sync="dialogVisible">
                <img width="100%" :src="dialogImageUrl" alt="">
            </el-dialog>
        </section>


    </div>
</template>

<script>
    export default {
        name: "index",

        data() {
            return {
                mallImgList: [{
                    name: 'food.jpeg',
                    url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
                }],
                // mallImgList: ['https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'],
                personImgList: [{
                    name: 'food.jpeg',
                    url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
                }, {
                    name: 'food2.jpeg',
                    url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
                }],

                dialogImageUrl: '',
                dialogVisible: false
            }
        },

        components: {},

        computed: {},

        methods: {
            handleRemove(file, fileList) {
                console.log(file, fileList);
            },
            handlePictureCardPreview(file) {
                console.log('[preview]',file);
                this.dialogImageUrl = file.url;
                this.dialogVisible = true;
            }
        },

        created() {
        },
    }
</script>

