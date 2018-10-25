<style lang="less" scoped>
    @import "../../common/css/index";

    .container{
        img{
            max-width:100%;
            max-height:100%;
        }
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <img src="/static/images/testbg.jpg" alt="">
        <a href="https://www.hzmyo.cn/ued/php/upload/20181011/1539237187747826.pdf">
            <img src="/static/images/testbg.jpg" style="width: 20px;height: 20px;" alt="">
            xx公司制度
        </a>
    </div>
</template>

<script>
    export default {
        name: "authorization",

        data() {
            return {}
        },

        components: {},

        methods: {},
    }
</script>

