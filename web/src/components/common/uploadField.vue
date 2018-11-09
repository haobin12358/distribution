<style lang="less" scoped>
    @import "../../common/css/index";

    .upload-field {
        padding: 24px;
        border-top: 1px solid @grayBorderColor;
        .fj(flex-start);
        align-items: center;
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

        .loading {
            margin: 0 5px;
            .wl(40px, 40px);
            display: inline-block;
            vertical-align: middle;
            animation: myLoading 1s steps(12, end) infinite;
            background: transparent url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjAiIGhlaWdodD0iMTIwIiB2aWV3Qm94PSIwIDAgMTAwIDEwMCI+PHBhdGggZmlsbD0ibm9uZSIgZD0iTTAgMGgxMDB2MTAwSDB6Ii8+PHJlY3Qgd2lkdGg9IjciIGhlaWdodD0iMjAiIHg9IjQ2LjUiIHk9IjQwIiBmaWxsPSIjRTlFOUU5IiByeD0iNSIgcnk9IjUiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgLTMwKSIvPjxyZWN0IHdpZHRoPSI3IiBoZWlnaHQ9IjIwIiB4PSI0Ni41IiB5PSI0MCIgZmlsbD0iIzk4OTY5NyIgcng9IjUiIHJ5PSI1IiB0cmFuc2Zvcm09InJvdGF0ZSgzMCAxMDUuOTggNjUpIi8+PHJlY3Qgd2lkdGg9IjciIGhlaWdodD0iMjAiIHg9IjQ2LjUiIHk9IjQwIiBmaWxsPSIjOUI5OTlBIiByeD0iNSIgcnk9IjUiIHRyYW5zZm9ybT0icm90YXRlKDYwIDc1Ljk4IDY1KSIvPjxyZWN0IHdpZHRoPSI3IiBoZWlnaHQ9IjIwIiB4PSI0Ni41IiB5PSI0MCIgZmlsbD0iI0EzQTFBMiIgcng9IjUiIHJ5PSI1IiB0cmFuc2Zvcm09InJvdGF0ZSg5MCA2NSA2NSkiLz48cmVjdCB3aWR0aD0iNyIgaGVpZ2h0PSIyMCIgeD0iNDYuNSIgeT0iNDAiIGZpbGw9IiNBQkE5QUEiIHJ4PSI1IiByeT0iNSIgdHJhbnNmb3JtPSJyb3RhdGUoMTIwIDU4LjY2IDY1KSIvPjxyZWN0IHdpZHRoPSI3IiBoZWlnaHQ9IjIwIiB4PSI0Ni41IiB5PSI0MCIgZmlsbD0iI0IyQjJCMiIgcng9IjUiIHJ5PSI1IiB0cmFuc2Zvcm09InJvdGF0ZSgxNTAgNTQuMDIgNjUpIi8+PHJlY3Qgd2lkdGg9IjciIGhlaWdodD0iMjAiIHg9IjQ2LjUiIHk9IjQwIiBmaWxsPSIjQkFCOEI5IiByeD0iNSIgcnk9IjUiIHRyYW5zZm9ybT0icm90YXRlKDE4MCA1MCA2NSkiLz48cmVjdCB3aWR0aD0iNyIgaGVpZ2h0PSIyMCIgeD0iNDYuNSIgeT0iNDAiIGZpbGw9IiNDMkMwQzEiIHJ4PSI1IiByeT0iNSIgdHJhbnNmb3JtPSJyb3RhdGUoLTE1MCA0NS45OCA2NSkiLz48cmVjdCB3aWR0aD0iNyIgaGVpZ2h0PSIyMCIgeD0iNDYuNSIgeT0iNDAiIGZpbGw9IiNDQkNCQ0IiIHJ4PSI1IiByeT0iNSIgdHJhbnNmb3JtPSJyb3RhdGUoLTEyMCA0MS4zNCA2NSkiLz48cmVjdCB3aWR0aD0iNyIgaGVpZ2h0PSIyMCIgeD0iNDYuNSIgeT0iNDAiIGZpbGw9IiNEMkQyRDIiIHJ4PSI1IiByeT0iNSIgdHJhbnNmb3JtPSJyb3RhdGUoLTkwIDM1IDY1KSIvPjxyZWN0IHdpZHRoPSI3IiBoZWlnaHQ9IjIwIiB4PSI0Ni41IiB5PSI0MCIgZmlsbD0iI0RBREFEQSIgcng9IjUiIHJ5PSI1IiB0cmFuc2Zvcm09InJvdGF0ZSgtNjAgMjQuMDIgNjUpIi8+PHJlY3Qgd2lkdGg9IjciIGhlaWdodD0iMjAiIHg9IjQ2LjUiIHk9IjQwIiBmaWxsPSIjRTJFMkUyIiByeD0iNSIgcnk9IjUiIHRyYW5zZm9ybT0icm90YXRlKC0zMCAtNS45OCA2NSkiLz48L3N2Zz4=) no-repeat;
            background-size: 100%;

            &.weui-loading_transparent {
                background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 100 100'%3E%3Cpath fill='none' d='M0 0h100v100H0z'/%3E%3Crect xmlns='http://www.w3.org/2000/svg' width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.56)' rx='5' ry='5' transform='translate(0 -30)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.5)' rx='5' ry='5' transform='rotate(30 105.98 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.43)' rx='5' ry='5' transform='rotate(60 75.98 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.38)' rx='5' ry='5' transform='rotate(90 65 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.32)' rx='5' ry='5' transform='rotate(120 58.66 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.28)' rx='5' ry='5' transform='rotate(150 54.02 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.25)' rx='5' ry='5' transform='rotate(180 50 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.2)' rx='5' ry='5' transform='rotate(-150 45.98 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.17)' rx='5' ry='5' transform='rotate(-120 41.34 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.14)' rx='5' ry='5' transform='rotate(-90 35 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.1)' rx='5' ry='5' transform='rotate(-60 24.02 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.03)' rx='5' ry='5' transform='rotate(-30 -5.98 65)'/%3E%3C/svg%3E");
            }
        }

        @keyframes myLoading {
            0% {
                transform: rotate3d(0, 0, 1, 0deg);
            }

            100% {
                transform: rotate3d(0, 0, 1, 360deg);
            }
        }

    }
</style>

<template>
    <section class="upload-field">
        <span class="label">{{label}}</span>
        <ul class="upload-imgs">
            <template v-if="readOnly">
                <li v-for="item,index in imgs" class="upload-imgs-item">
                    <img class="evidence-img" :src="item" alt="">
                </li>
            </template>
            <template v-else>
                <li v-for="item,index in blobImgs" class="upload-imgs-item">
                    <img class="evidence-img" :src="item" alt="">
                    <img @click="removeImg(index)" class="img-block-close" src="/static/images/close.png" alt="">
                </li>
            </template>

            <li v-if="!readOnly && blobImgs.length < uploadLimit" class="upload-imgs-item-placeholder ">
                <img src="/static/images/img-placeholder.png" alt="">
                <input class="picture-file" id="up-picture-file" type="file" accept="image/*" ref="file"
                       @change="uploadFile">
            </li>
        </ul>
        <div class="loading" v-if="someImgIsLoading"></div>
    </section>
</template>

<script>
    import {title, removeFile} from "src/api/api"
    import Axios from "axios"
    import {setStore, getStore} from "src/common/js/mUtils"
    import {TOKEN} from "src/common/js/const"

    export default {
        name: "uploadField",

        props: {
            //  表单项标题
            label: {
                type: String
            },
            //  readonly为false时  显示不用imgs
            imgs: {
                type: Array
            },
            //  只显示,不能上传修改
            readOnly: {
                type: Boolean,
                default: true
            },
            uploadLimit: {
                type: Number,
                default: 2
            }
        },

        data() {
            return {
                // readonly为false时  显示用
                blobImgs: [],
                //  readonly为false时  关联用
                blobLinkImgs: {},
                blobLinkTokenImgs: {},
                //  是否有token    为私有文件
                haveToken: false
            }
        },

        components: {},

        computed: {
            someImgIsLoading() {
                let imgs = []
                if (!this.readOnly) {

                    for (let i = 0; i < this.blobImgs.length; i++) {
                        imgs.push(this.blobLinkImgs[this.blobImgs[i]]);

                        if (!this.blobLinkImgs[this.blobImgs[i]]) {
                            this.$emit('isUploading', true);
                            return true;
                        }
                    }

                    this.$emit('update', imgs);
                    this.$emit('isUploading', false);
                    return false;
                }
            }
        },

        watch: {},

        methods: {
            removeImg(index) {
                let removeBlockImgUrl = this.blobImgs.splice(index, 1)[0],
                    removeImgUrl = this.blobLinkImgs[removeBlockImgUrl],
                    removeImgToken = this.blobLinkTokenImgs[removeBlockImgUrl];

                removeImgUrl = removeImgUrl.split('file/')[1]

                if (this.haveToken) {
                    removeFile(removeImgUrl, getStore(TOKEN)).then();
                } else {
                    // removeFile(removeImgUrl, removeImgToken).then();
                }
            },
            uploadFile() {
                let file = this.$refs.file.files[0];
                let blobImgUrl = '';    //  访问本机图片用
                let formData = new FormData();

                //  只读不允许上传
                if (this.readOnly) {
                    return
                }

                if (file.size / (1024 * 1024) > 10) {
                    this.$toast('图片过大');
                    return
                }

                formData.append('file', file);
                blobImgUrl = window.URL.createObjectURL(this.$refs.file.files[0]);
                this.blobImgs.push(blobImgUrl);
                let newImgIndex = this.blobImgs.indexOf(blobImgUrl);
                this.$set(this.blobLinkImgs, blobImgUrl, '');

                document.getElementsByClassName('picture-file')[0].value = '';
                Axios({
                    url: title + '/user/upload_file',
                    params: {
                        token: getStore(TOKEN)
                    },
                    method: 'post',
                    data: formData,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                }).then(
                    ({data: resData}) => {
                        if (resData.status == 200) {
                            if (this.haveToken) {
                                this.blobLinkImgs[blobImgUrl] = resData.data;
                            } else {
                                this.blobLinkImgs[blobImgUrl] = resData.data.url;
                                this.blobLinkTokenImgs[blobImgUrl] = resData.data.token;
                            }
                        } else {
                            this.$toast({
                                message: '凭证上传失败,请重新上传图片:' + file.name,
                                position: 'bottom',
                            });
                            this.blobImgs.splice(newImgIndex, 1);
                        }
                    }
                ).catch(
                    res => {
                        this.$toast({
                            message: '凭证上传失败,请重新上传图片:' + file.name,
                            position: 'bottom',
                        });
                        this.blobImgs.splice(newImgIndex, 1);
                    }
                );
            }
        },

        created() {
            this.haveToken = !!getStore(TOKEN);
        },
    }
</script>

