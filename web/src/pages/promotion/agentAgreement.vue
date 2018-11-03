<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();

        .agreement {
            padding: 20px 20px 100px;
            border-bottom: 1px solid @mainFontColor;

            .title {
                font-size: large;
                font-weight: bold;
                text-align: center;
                margin-bottom: 50px;
            }

            h1.small-title {
                font-weight: bold;

            }

            p {
                text-indent: 2em;
            }

            p.stress {
                font-weight: bold;

            }
        }

        .action-block {
            padding-top: 40px;
            text-align: center;
            .fj();
            flex-direction: column;

            .check-label {
                .fz(28px);

                input[type=checkbox] {
                    -webkit-appearance: checkbox;
                }
            }

            .button {
                /*background: transparent;*/
            }
        }
    }
</style>

<template>
    <div class="container">
        <header-top></header-top>

        <article class="agreement">
            <h1 class="title">代理协议</h1>
            <h1 class="small-title">
                1.xx
            </h1>
            <p>这是一段这是一段这是一段这是一段这是一段这是一段这是一段这是一段这是一段这是一段这是一段这是一段这是一段这是一段</p>
            <p class="stress">这是一段强调文本</p>
            <p>这是一段</p>
            <p>这是一段</p>
            <h1 class="small-title">
                2.xx
            </h1>
            <p>这是一段</p>
            <p>这是一段</p>
        </article>

        <section class="action-block">
            <label class="check-label"><input name="agree" v-model="agree" type="checkbox" value="1"/> 同意签署此协议内容</label>

            <section class="my-confirm-btn-wrap" style="margin-top: 20px">
                <button class="my-confirm-btn" @click="doConfirm">同意提交</button>
            </section>
        </section>
    </div>
</template>

<script>
    import {setStore, getStore} from "src/common/js/mUtils"
    import {TOKEN, AGREE_AGENT_AGREEMENT_EXP} from "src/common/js/const"
    import {checkQrcode} from "src/api/api"


    export default {
        name: "agentAgreement",

        data() {
            return {
                agree: [],

                canUse: false,
                cantUseInfo: ''
            }
        },

        watch: {},

        components: {},

        computed: {},

        methods: {
            doConfirm() {
                if (this.agree[0]) {
                    if (this.canUse) {
                        setStore(AGREE_AGENT_AGREEMENT_EXP, new Date().toLocaleString('zh-CN', {hour12: false}));
                        this.$router.push('/applyAgent?QRid=' + this.$route.query.QRid)
                    } else {
                        this.$toast(this.cantUseInfo);
                    }
                } else {
                    this.$toast('请先同意签署此协议!');
                }
            }
        },

        async created() {

            if (getStore(AGREE_AGENT_AGREEMENT_EXP) && new Date() - new Date(getStore(AGREE_AGENT_AGREEMENT_EXP)) < 30 * 1000) {
                this.$router.push('/applyAgent?QRid=' + this.$route.query.QRid)
                this.$toast('你已同意协议');
            }

            let resData = await checkQrcode(this.$route.query.QRid);

            if (resData) {
                if (resData.data.QRnumber < 1) {
                    this.canUse = false
                    this.cantUseInfo = '二维码次数用完'
                } else if (new Date() > new Date(resData.data.QRovertime)) {
                    this.canUse = false
                    this.cantUseInfo = '二维码已过期'
                } else {
                    this.canUse = true
                }
            }
        },
    }
</script>

