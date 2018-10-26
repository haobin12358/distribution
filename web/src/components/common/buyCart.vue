<style lang="less" scoped>
    @import "../../common/css/index";

    .buy-cart{
        .fj();
        align-items: center;

        .buy-cart-btn{
            .wl(40px, 40px);
        }

        .buy-cart-num{
            margin:  0 17px;

        }
    }

    .showReduce-enter-active, .showReduce-leave-active {
        transition: all .3s ease-out;
    }
    .showReduce-enter, .showReduce-leave-active {
        opacity: 0;
        transform: translateX(1rem);
    }

    .hide-enter-active,.hide-leave-active{
        transition: opacity .3s;
    }

    .hide-enter,.hide-leave-to{
        opacity: 0;
    }
</style>

<template>
    <section class="buy-cart">
        <transition name="showReduce">
            <img class="buy-cart-btn" src="/static/images/minus.png" v-if="shopNum"  @click="minus" alt="">
        </transition>

        <transition name="hide">
            <span class="buy-cart-num" v-if="shopNum">{{shopNum}}</span>
        </transition>

        <img class="buy-cart-btn" src="/static/images/add.png" @click="add" alt="">
    </section>
</template>

<script>
    export default {
        name: "buy-cart",

        props: ['shopNum'],

        data() {
            return {
            }
        },

        components: {},

        methods: {
            minus(){
                this.$emit('minus');
            },
            add(){
                this.$emit('add');
            }
        },
    }
</script>

