<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        button{
            .wl(364px, 90px);
            background: linear-gradient(180deg, @mainLightColor 0%, @mainColor 100%);
            .sc(38px, white);
            .fontc(90px);
            font-weight: bold;
            border-radius: 50px;
            border: none;
            display: block;
            margin: 0 auto;
        }
    }
</style>

<template>
    <div class="container" >
        <button @click="$emit('click')">{{text}}</button>
    </div>
</template>

<script>
    export default {
        name: "bigBtn",

        props:{
           text: ''
        },

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

