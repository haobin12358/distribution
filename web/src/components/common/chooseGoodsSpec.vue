<style lang="less" scoped>
    @import "../../common/css/index";

</style>

<template>

</template>

<script>
    import Count from "src/components/common/count";

    export default {
        name: "chooseGoodsSpec",

        components: {
            Count
        },

        props: {
            popupVisible:{
                type: Boolean,
            }
        },

        data() {
            return {
            }
        },

        computed: {},

        methods: {
            close(){
                console.log('closeonclick');
            }
        },

        created() {

        },
    }
</script>

