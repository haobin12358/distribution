<style lang="less" scoped>
    @import "~common/css/index";

    .messageDetail {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: white;
        z-index: 10;

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

            .sub-title{
                font-weight: bold;
            }
        }

        .msg-content{
            .fz(26px);

        }
    }
</style>

<template>
    <div class="messageDetail">
        <header-top :title="'公司消息详情'"></header-top>

        <header class="title">
            {{readingMessage.title}}
        </header>

        <section class="sub-header">
            <span class="sub-title">公告</span>
            <span> {{readingMessage.date}}</span>
        </section>

        <article class="msg-content">
            {{readingMessage.content}}
        </article>
    </div>
</template>

<script>
    import {mapState, mapMutations} from 'vuex'

    export default {
        name: "messageDetail",

        data() {
            return {}
        },

        computed: {
            ...mapState(['readingMessage'])

        },

        components: {},

        methods: {},
    }
</script>

