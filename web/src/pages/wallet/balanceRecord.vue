<style lang="less" scoped>
    @import "../../common/css/index";

    .container{
        #go-charge-record{
            .wl(33px, 27px);
        }
    }
</style>

<template>
    <div class="container">
        <header-top :title="$route.meta.title" :show-back="true">
            <section slot="right">
                <img id="go-charge-record" src="/static/images/myOrder.png" alt="">
            </section>
        </header-top>
    </div>
</template>

<script>
    export default {
        name: "chargeRecord",

        data() {
            return {}
        },

        components: {},

        methods: {},
    }
</script>

