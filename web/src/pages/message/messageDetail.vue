<style lang="less" scoped>
    @import "../../common/css/index";

    .messageDetail {
        .least-full-screen();

        .title {
            text-align: center;
            font-weight: bold;
            .fz(36px);
            margin-bottom: 30px;
        }

        .sub-header {
            .fj();
            align-items: center;
            margin-bottom: 20px;
            padding: 0 20px;
            .fz(26px);

            .sub-title {
                font-weight: bold;
            }
        }

        .msg-content {
            .fz(26px);
            text-align: center;

            .content-is-doc{
                text-indent: 2em;
                text-align: left;
                .fz(32px);
                img{
                    .wl(32px, 32px);
                }
            }
            img.content-is-img {
                max-width: 100%;
                max-height: 100%;
            }
        }
    }
</style>

<template>
    <section class="messageDetail">
        <header-top :title="'公司消息详情'" :show-back="true"></header-top>

        <header class="title">
            {{message.CMtitle}}
        </header>

        <section class="sub-header">
            <span class="sub-title">公告</span>
            <span> {{message.CMdate}}</span>
        </section>

        <article class="msg-content">
            <section class="content-is-doc" v-if="isDoc">
                <img src="/static/images/pdf.png" alt="">
                <a :href="message.CMfile">{{fullFileName}}</a>
            </section>
            <img class="content-is-img" v-else :src="message.CMfile" alt="">
        </article>
    </section>
</template>

<script>
    import {mapState, mapMutations} from 'vuex'
    import BScroll from 'better-scroll'
    import {getCommessageDetails} from "src/api/api"

    export default {
        name: "messageDetail",

        data() {
            return {
                message: {},
                isDoc: true,    //  文档或者图片
                fullFileName: '',   // 拼接出文件名

            }
        },

        computed: {},

        components: {},

        methods: {
            gotoFilePage(){
                location.href = 'https://www.hzmyo.cn/ued/php/upload/20181011/1539237187747826.pdf';
            },
        },

        mounted() {

        },

        created() {
            this.message = this.$route.query;

            // 处理未读
            if (this.message.isread == 0) {
                getCommessageDetails(this.message.CMid);
            }

            if (this.message.CMfile) {
                let lastDotIndex = this.message.CMfile.lastIndexOf('.'),
                    fullNameSuffix = this.message.CMfile.substring(lastDotIndex + 1);

                if (['img', 'jpg', 'gif', 'jpeg', 'bmp'].includes(fullNameSuffix)) {
                    this.isDoc = false;
                }
                this.fullFileName = this.message.CMtitle + '.' + fullNameSuffix;
            }
        }
    }
</script>

