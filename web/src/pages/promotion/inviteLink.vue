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
        <header-top :show-back="showBack()"></header-top>

        <section class="invite-code-wrap">
            <!--<img src="/static/images/testbg.jpg" @click="$router.push('/applyAgent')" alt="" class="invite-code-img">-->
            <vue-qr :text="code" :size="300" :margin="0" class="invite-code-img"></vue-qr>

            <p class="tip">链接：{{code}}</p>
            <p class="tip">说明：长按二维码图片下载</p>
        </section>
    </div>
</template>

<script>
    import VueQr from 'vue-qr'
    import {setStore, getStore} from "src/common/js/mUtils"
    import {TOKEN} from "src/common/js/const"

    export default {
        name: "inviteLink",

        data() {
            return {
                code: ''
            }
        },

        components: {
            VueQr
        },

        computed: {},

        methods: {
            showBack(){
                return !!getStore(TOKEN)
            }
        },

        created() {
            this.code =this.$route.query.code;
        },
    }
</script>

