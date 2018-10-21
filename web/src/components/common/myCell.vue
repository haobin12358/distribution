<style lang="less" scoped>
    @import "../../common/css/index";

    .my-cell {
        .fj();
        .bgw();
        .fz(32px);
        padding: 20px 20px;

        .my-cell-title {
            white-space: nowrap;
            margin-right: 90px;
            width: 130px;

        }

        .my-cell-value {
            flex: 1;

            &.readonly{
                color: #777777;
            }
        }
    }
</style>

<template>
    <div class="my-cell">
        <p class="my-cell-title">{{title}}</p>
        <p :class="{'my-cell-value': true, 'readonly': readonly}">{{value}}</p>
    </div>
</template>

<script>
    export default {
        name: "myCell",

        props: ['title', 'value', 'readonly'],

        data() {
            return {
            }
        },

        components: {},

        computed: {},

        methods: {},

        created() {
        },
    }
</script>

