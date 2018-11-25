<style lang="less" scoped>
    @import "../../common/css/index";

    .buy-cart {
        .fj();
        align-items: center;

        .buy-cart-btn {
            .wl(50px, 50px);
        }

        .buy-cart-num {
            margin: 0 16px;
            .fz(28px);
            width: 66px;
            text-align: center;
            border: 2px solid @mainColor;
            border-radius: 10px;

        }
    }

    .showReduce-enter-active, .showReduce-leave-active {
        transition: all .3s ease-out;
    }

    .showReduce-enter, .showReduce-leave-active {
        opacity: 0;
        transform: translateX(1rem);
    }

    .hide-enter-active, .hide-leave-active {
        transition: opacity .3s;
    }

    .hide-enter, .hide-leave-to {
        opacity: 0;
    }
</style>

<template>
    <section class="buy-cart">
        <transition name="showReduce">
            <img class="buy-cart-btn" src="/static/images/minus.png"
                 v-if="shopItem.PRnum"
                 @click.stop="minus" alt="">

        </transition>

        <transition name="hide">

            <input class="buy-cart-num"
                   v-if="shopItem.PRnum"
                   type="number"
                   onkeyup="value=value.replace(/[^\d]/g,'')"
                   v-bind="$attrs"
                   v-bind:value="shopItem.PRnum"
                   v-on:blur="$emit('input', $event.target.value)"

            />
        </transition>
        <img class="buy-cart-btn" src="/static/images/add.png" @click.stop="add" alt="">
    </section>
</template>

<script>
    export default {
        name: "buy-cart",

        props: ['shopItem'],

        data() {
            return {}
        },

        components: {},


        methods: {
            minus() {
                this.$emit('minus');
            },
            add() {
                this.$emit('add');
            }
        },
    }
</script>

