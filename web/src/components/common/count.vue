<style lang="less" scoped>
    @import "../../common/css/index";

    .count {
        .fj();
        align-items: center;

        .count-btn {
            .wl(44px, 44px);

            &.disable{
                opacity: .7;
            }

        }

        .count-num {
            margin: 0 16px;
            .fz(28px);
            width: 78px;
            height: 40px;
            text-align: center;
            border: 2px solid @mainColor;
            border-radius: 10px;

        }
    }

    .showReduce-enter-active, .showReduce-leave-active {
        transition: all .3s ease-out;
    }

    .showReduce-enter, .showReduce-leave-active {
        opacity: .7;
        /*transform: translateX(66px);*/
    }

    .hide-enter-active, .hide-leave-active {
        transition: opacity .3s;
    }

    .hide-enter, .hide-leave-to {
        opacity: 0;
    }
</style>

<template>
    <section class="count">
        <img :class="{'count-btn': true,  'disable': count == 0}" src="/static/images/minus.png"
             @click.stop="minus" alt="">

        <input class="count-num"
               type="number"
               onkeyup="value=value.replace(/[^\d]/g,'')"
               v-bind="$attrs"
               v-bind:value="count"
               v-on:blur="$emit('input', $event.target.value)"
        />
        <img class="count-btn" src="/static/images/add.png" @click.stop="add" alt="">
    </section>
</template>

<script>
    export default {
        name: "count",

        props: {
            count: {
                type: Number,
                default: 1
            }
        },

        data() {
            return {}
        },

        components: {},


        methods: {
            minus() {
                if(this.count > 0){
                    this.$emit('minus');
                }
            },
            add() {
                this.$emit('add');
            }
        },
    }
</script>

