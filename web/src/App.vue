<template>
    <div id="app">
        <transition :name=" 'router-fade'">
            <keep-alive>
                <router-view v-if="$route.meta.keepAlive"></router-view>
            </keep-alive>
        </transition>
        <transition :name="'router-fade'" mode="out-in">
            <router-view v-if="!$route.meta.keepAlive"></router-view>
        </transition>
    </div>
</template>

<script>
    import {setStore, getStore} from "src/common/js/mUtils"
    import {TOKEN,ALL_AREA} from "src/common/js/const"
    import {getAllArea} from "src/api/api"

    export default {
        name: 'App',
        created(){
            this.$store.commit('INIT_CART');
            this.$store.commit('INIT_USER_INFO');
            if(!getStore(ALL_AREA)){
                getAllArea().then(
                    ({data})=>{
                        setStore(ALL_AREA, data);
                    }
                )
            }
        }
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
        transition: opacity .1s;
    }

    .router-fade-enter {
        opacity: 0;
    }

    .router-slid-enter-active {
        transition: all .3s;
    }

    .router-slid-enter, .router-slid-leave-active {
        transform: translate3d(2rem, 0, 0);
        opacity: 0;
    }

    .router-slid-reverse-enter-active{
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

        background: url("/static/images/success.svg");
        background-size: cover;
        width: 100px;
        height: 100px;
        overflow: hidden;
    }

    /*.m-toast-audit{*/
        /*background: url("/static/images/toast_audit.png");*/
        /*background-size: cover;*/
        /*width: 169px;*/
        /*height: 169px;*/
        /*overflow: hidden;*/
    /*}*/

    /*.m-toast-audit-bg{*/
        /*background: white;*/
        /*color: #6EABB8;*/
        /*font-weight: bold;*/
    /*}*/
</style>
