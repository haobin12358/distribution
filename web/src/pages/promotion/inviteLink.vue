<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();

        .invite-code-wrap{
            padding: 0 67px;

            .invite-code-img{
                display: block;
                margin: 80px auto 35px;
                .wl(617px,617px);
            }

            .tip{
                .fz(28px);

                &:first-child{
                    margin-bottom: 16px;
                }
            }
        }
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <section class="invite-code-wrap">
            <img src="/static/images/testbg.jpg" @click="$router.push('/applyAgent')" alt="" class="invite-code-img">

            <p class="tip">链接：http://www.zhelishiwoluanxiede.cm</p>
            <p class="tip">说明：长按二维码图片下载</p>
        </section>
    </div>
</template>

<script>
    export default {
        name: "inviteLink",

        data() {
            return {}
        },

        components: {},

        computed: {},

        methods: {},

        created() {
        },
    }
</script>

