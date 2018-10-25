<style lang="less" scoped>
    @import "../../common/css/index";

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
</style>

<template>
    <section class="upload-field">
        <span class="label">{{label}}</span>
        <ul class="upload-imgs">
            <li class="upload-imgs-item">
                <img class="evidence-img" src="/static/images/testbg.jpg" alt="">


                <img class="img-block-close" src="/static/images/close.png" alt="">
            </li>
            <li class="upload-imgs-item-placeholder ">
                <img src="/static/images/img-placeholder.png" alt="">
                <input class="picture-file" id="up-picture-file" type="file" accept="image/*" ref="file"
                       @change="uploadFile">
            </li>
        </ul>
    </section></template>

<script>
    export default {
        name: "uploadField",

        props:{
            label:{
                type: String
            }
        },

        data() {
            return {}
        },

        components: {},

        computed: {},

        methods: {
            uploadFile() {
                console.log(this.$refs.file.files[0]);
            }
        },

        created() {
        },
    }
</script>

