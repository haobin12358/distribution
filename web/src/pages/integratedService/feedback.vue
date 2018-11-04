<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();

        .tip{
            margin: 20px 0 10px 25px;
        }

        .textarea{
            .wl(750px, 490px);
            padding: 20px;
            box-sizing: border-box;
            .fz(28px);
        }
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <p class="tip">
            为了给您更好的用户体验，我们期待您的反馈，谢谢！
        </p>

        <textarea class="textarea" placeholder="请填写您的建议和意见" id="" cols="30" rows="10"></textarea>

        <section class="my-confirm-btn-wrap" style="margin-top: 174px;">
            <button class="my-confirm-btn">提 交 建 议</button>
        </section>
    </div>
</template>

<script>
    export default {
        name: "feedback",

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

