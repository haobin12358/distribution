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
        <upload-new-head-img label="新头像" :readOnly="false" :imgs.sync="newHeadImgs"
                             :upload-limit="1"></upload-new-head-img>

        <img src="/static/../../testbg.jpg" style="width: 200px;height:  200px;" alt="">
        <section class="my-confirm-btn-wrap">
            <button class="my-confirm-btn">确 认</button>
        </section>
    </div>
</template>

<script>
    import UploadField from "src/components/common/uploadField"

    export default {
        name: "changeHeadImg",

        data() {
            return {
                oldHeadImgs: ['/static/images/testbg.jpg'],
                newHeadImgs: [],
            }
        },

        components: {
            UploadOldHeadImg: UploadField,
            UploadNewHeadImg: UploadField,
        },

        computed: {},

        methods: {},

        created() {
        },
    }
</script>

