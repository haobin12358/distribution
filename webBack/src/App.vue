<template>
    <div id="app">
        <keep-alive>
            <router-view v-if="$route.meta.keepAlive"></router-view>
        </keep-alive>
        <router-view v-if="!$route.meta.keepAlive"></router-view>
    </div>
</template>

<script type="text/ecmascript-6">
    export default {
        name: 'App',

        created(){
            document.title = '蓓莉云仓后台管理系统'
        }
    }
</script>

<style lang="less" rel="stylesheet/less" scoped>
    @import "common/css/_variate";

    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        /*text-align: center;*/
        color: #2c3e50;
        min-height: 100%;
        background-color: #ffffff;
        /*margin-top: 60px;*/
    }
</style>
