<style lang="less" scoped>
    @import "~common/css/index";

    .messageDetail {
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

        }
    }
</style>

<template>
    <section class="messageDetail">
        <header-top :title="'公司消息详情'" :show-back="true"></header-top>

        <header class="title">
            {{readingMessage.title}}
        </header>

        <section class="sub-header">
            <span class="sub-title">公告</span>
            <span> {{readingMessage.date}}</span>
        </section>

        <article class="msg-content" v-for="item in 100">
            <!--{{readingMessage.content}}-->
            {{item}}
        </article>
    </section>
</template>

<script>
    import {mapState, mapMutations} from 'vuex'
    import BScroll from 'better-scroll'

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

        mounted() {

        }
    }
</script>

