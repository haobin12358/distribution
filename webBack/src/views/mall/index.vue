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
                云仓轮播图(限一张)
            </header>

            <el-upload
                class="swiper-uploader"
                :action="uploadUrl"
                accept="image/*"
                list-type="picture-card"
                :file-list="mallImgList"
                :on-success="handleMallImgSuccess"
                :on-preview="handlePictureCardPreview"
                :before-upload="beforeAvatarUpload"

                :on-remove="handleRemove"
                :limit="1">
                <i class="el-icon-plus"></i>
                <div slot="tip" class="el-upload__tip">建议宽高比为2.6(375/145),大小不要超过10M,上传成功后会显示,上传大图请耐心等待</div>

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
                :action="uploadUrl"
                accept="image/*"
                list-type="picture-card"
                :file-list="personImgList"
                :on-success="handlePersonImgSuccess"
                :on-preview="handlePictureCardPreview"
                :before-upload="beforeAvatarUpload"
                :on-remove="handleRemove"
                :http-request="uploadPersonImgs"
                :multiple="true">
                <i class="el-icon-plus"></i>
                <div slot="tip" class="el-upload__tip">建议宽高比为2.6(375/145),大小不要超过10M,上传成功后会显示,上传大图请耐心等待,可多选</div>
            </el-upload>
            <el-dialog :visible.sync="dialogVisible">
                <img width="100%" :src="dialogImageUrl" alt="">
            </el-dialog>
        </section>


    </div>
</template>

<script>
    import {mapState} from "vuex";

    export default {
        name: "index",

        data() {
            return {
                mallImgList: [],
                personImgList: [],

                dialogImageUrl: '',
                dialogVisible: false
            }
        },

        components: {},

        computed: {
            uploadUrl() {
                return this.$api.uploadFile + localStorage.getItem('token');
            }
        },

        methods: {
            handleRemove(file, fileList) {
                this.$confirm(`确定要删除该图?`, '提示', {
                    type: 'warning'
                }).then(
                    () => {
                        this.$http.post(this.$api.deleteSowingMap, {
                            smid: file.uid
                        }, {
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
                                        title: '轮播图删除成功',
                                        type: 'success'
                                    });
                                }
                            }
                        )
                    }).catch(e => {
                    this.setData();
                })

            },


            handlePictureCardPreview(file) {
                console.log('[preview]', file);
                this.dialogImageUrl = file.url;
                this.dialogVisible = true;
            },

            setData() {
                this.$http.get(this.$api.getSowingMap,
                    {
                        params: {
                            token: this.$common.getStore('token')
                        }
                    }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                                this.mallImgList = data.mallUrls.map(item => {
                                        return {
                                            url: item.SMurl,
                                            uid: item.SMid,
                                        };
                                    }
                                );

                                this.personImgList = data.personUrls.map(item => {
                                        return {
                                            url: item.SMurl,
                                            uid: item.SMid,
                                        };
                                    }
                                )

                        }
                    }
                )
            },

            beforeAvatarUpload(file) {
                const isLt15M = file.size / 1024 / 1024 < 10;

                if (!isLt15M) {
                    this.$message.error('上传轮播图片大小不能超过 10MB!');
                }

                return isLt15M;
            },

            //  云仓图上传成功
            handleMallImgSuccess(response, file, fileList) {
                //  显示
                this.mallImgList = fileList.map(item => {
                    let res = {
                        name: item.name,
                        url: item.url,
                    }

                    if (item.response && item.response.data) {
                        //  替换掉blob
                        res.url = item.response.data;
                    }

                    return res;
                });

                this.$http.post(this.$api.addSowingMap, {
                    "type": 2,
                    "urls": this.mallImgList.map(item => item.url), //  数据格式
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
                                title: '云仓图已更新',
                                type: 'success'
                            });
                        }
                    }
                );
            },

            addPersonImgSowingMap() {
                this.$http.post(this.$api.addSowingMap, {
                    "type": 1,
                    "urls": this.personImgList.map(item => item.url),
                }, {
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
                                title: '个人轮播图已更新',
                                type: 'success'
                            });
                        }
                    }
                );
            },


            uploadPersonImgs(file) {
                console.log(file);
                let formData = new FormData();

                formData.append('file', file.file)

                this.$http({
                    url: file.action,
                    params: {
                        token: this.$common.getStore('token')
                    },
                    method: 'post',
                    data: formData,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = resData.data;

                            this.personImgList.push({
                                name: file.file.name,
                                url: data
                            })
                            this.addPersonImgSowingMap();
                        }
                    }
                )

            },
        },

        created() {
            this.setData();
        },
    }
</script>

