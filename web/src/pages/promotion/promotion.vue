<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .bgw();
        .least-full-screen();

    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true">
              </header-top>

        <section class="my-confirm-btn-wrap">
            <router-link to="/wantInvite" tag="button" class="my-confirm-btn">代 理 招 募</router-link>
        </section>
    </div>
</template>

<script>
    import bigBtn from "src/components/common/bigBtn"

    export default {
        name: "promotion",

        data() {
            return {}
        },

        components: {
            bigBtn
        },

        methods: {},
    }
</script>

