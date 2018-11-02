<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();

        .upload-field {
            padding: 24px;
            border-top: 1px solid @grayBorderColor;
            .fj(flex-start);
            .bgw();

            .label {
                font-size: 32px;
                min-width: 240px;

            }

            .upload-imgs {
                .fj(flex-start);

                .upload-imgs-item {
                    .wl(123px, 123px);
                    margin-right: 30px;
                    position: relative;

                    img.evidence-img {
                        .wl(100%, 100%);
                    }

                    .img-block-close {
                        position: absolute;
                        width: 40px;
                        height: 40px;
                        right: -20px;
                        top: -20px;
                    }

                }

                .upload-imgs-item-placeholder {
                    position: relative;
                    .wl(123px, 123px);
                    border: 2px dotted @lightFontColor;

                    img {
                        position: absolute;
                        left: 50%;
                        top: 50%;
                        transform: translate(-50%, -50%);
                        .wl(47px, 47px);
                    }

                    input[type=file] {
                        position: absolute;
                        width: 100%;
                        height: 100%;
                        left: 0;
                        top: 0;
                        opacity: 0;
                    }
                }
            }

        }

    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <upload-old-head-img label="头像" :imgs="oldHeadImgs"></upload-old-head-img>
        <upload-new-head-img label="新头像" :readOnly="false" @update="updateNewHeadImg" @isUploading="listenUpload"
                             :upload-limit="1"></upload-new-head-img>

        <section class="my-confirm-btn-wrap">
            <button v-if="isImgUploading" class="my-confirm-btn disabled">头 像 上 传 中...</button>
            <button v-else @click="doConfirm" class="my-confirm-btn">确 认</button>
        </section>
    </div>
</template>

<script>
    import UploadField from "src/components/common/uploadField"
    import {updateHeadImg} from "src/api/api"
    import {mapActions} from "vuex"


    export default {
        name: "changeHeadImg",

        data() {
            return {
                oldHeadImgs: [],
                newHeadImgs: [],

                isImgUploading: true
            }
        },

        components: {
            UploadOldHeadImg: UploadField,
            UploadNewHeadImg: UploadField,
        },

        computed: {},

        methods: {
            ...mapActions(['getUserInfo']),
            updateNewHeadImg(imgs){
                this.newHeadImgs = imgs;
            },
            listenUpload(bool){
                this.isImgUploading = bool;
            },
            doConfirm(){
                if(this.newHeadImgs[0]){
                    updateHeadImg(this.newHeadImgs[0]).then(
                        data=>{
                            if(data){
                                this.$toast('修改成功');
                                this.getUserInfo();

                                this.$router.back();
                            }
                        }
                    )
                }else{
                    this.$toast('请选择要上传的头像!');
                }
            }
        },

        created() {
            this.oldHeadImgs[0] = this.$store.state.userInfo.USheadimg;
        },
    }
</script>

