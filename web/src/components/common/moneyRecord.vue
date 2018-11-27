<style lang="less" scoped>
    @import "../../common/css/index";
</style>

<template>
    <ul class="money-record">
        <li class="money-record-item" v-for="item in list" @click="clickHandler(item)">
            <p class="row">
                <span class="hard">{{item.type}}</span>
                <span class="weak">{{item.date}}</span>
            </p>
            <p class="row">
                <span class="weak">{{item.sn}}</span>
                <span class="hard">{{item.price}}</span>
            </p>

        </li>
    </ul>
</template>

<script>
    export default {
        name: "moneyRecord",

        props:{
          list: {
              type: Array,
              default:[]
          }
        },

        data() {
            return {}
        },

        components: {},

        methods: {
            clickHandler(item){
                this.$emit('clickItem', item)
            }
        },
    }
</script>

