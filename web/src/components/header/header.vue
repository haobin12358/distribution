<style lang="less" scoped>
    @import "../../common/css/index";

    .my-header{
        padding-top: 80px;
    }
</style>

<template>
    <div class="my-header">
        <mt-header :title="title || $route.meta.title" :fixed="true">

            <section slot="left" >
                <mt-button v-if="showBack" @click="goBack" icon="back"></mt-button>
                <slot name="left"></slot>
            </section>
            <section slot="right">
                <slot name="right"></slot>
            </section>
        </mt-header>
    </div>
</template>

<script>
    export default {
        name: "headerTop",

        props: {
            title: {
                type: String,
            },
            showBack: {
                type: Boolean
            }
        },

        data() {
            return {}
        },

        components: {},

        methods: {
            goBack() {
                this.$router.back();
            }
        },
    }
</script>

