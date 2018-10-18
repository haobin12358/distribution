<style lang="less" scoped>
    @import "../../common/css/index";

</style>

<template>
    <div class="container">
        <header-top :title="$route.meta.title" :show-back="true">
            <section slot="right">
                <router-link tag="button" to="/withdrawCash" class="go-withdraw-cash">提现</router-link>
            </section>
        </header-top>
    </div>
</template>

<script>
    export default {
        name: "withdrawCash",

        data() {
            return {}
        },

        components: {},

        methods: {},
    }
</script>

