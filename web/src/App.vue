<template>
    <div id="app">
        <transition name="router-fade" mode="out-in">
            <keep-alive>
                <router-view v-if="$route.meta.keepAlive"></router-view>
            </keep-alive>
        </transition>
        <transition name="router-fade" mode="out-in">
            <router-view v-if="!$route.meta.keepAlive"></router-view>
        </transition>
    </div>
</template>

<script>
    export default {
        name: 'App'
    }
</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        color: #333333;
        height: 100%;
        font-size: 24px;
        background: #eeeeee;
    }

    .router-fade-enter-active {
        transition: opacity .3s;
    }

    .router-fade-enter {
        opacity: 0;
    }

    .router-slid-enter-active, .router-slid-leave-active {
        transition: all .3s;
    }

    .router-slid-enter, .router-slid-leave-active {
        transform: translate3d(2rem, 0, 0);
        opacity: 0;
    }

    .router-slid-reverse-enter-active, .router-slid-reverse-leave-active {
        transition: all .3s;
    }

    .router-slid-reverse-enter, .router-slid-reverse-leave-active {
        transform: translate3d(-2rem, 0, 0);
        opacity: 0;
    }



    .m-toast-success {
        /*background-size: 100% 100%;*/
        /*width: 220px;*/
        /*height: 255px;*/
        /*background: url("/static/images/success.svg") no-repeat;*/

        background: url("/static/images/toast_success.png");
        background-size: cover;
        width: 100px;
        height: 100px;
        overflow: hidden;
    }
</style>
