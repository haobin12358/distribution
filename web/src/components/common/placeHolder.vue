<style lang="less" scoped>
    @import "../../common/css/index";

    .place-holder {
        height: 50vh;
        .m-flex-center();
        flex-direction: column;
        text-align: center;

        img{
            .wl(300px, 300px);
        }

        .placeholder-tip {
            margin-top: 30px;
            .fz(30px);
            text-align: center;
        }
    }
</style>

<template>
    <div class="place-holder">
        <div>
            <img :src="img" alt="">
            <div class="placeholder-tip">{{title}}</div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "placeHolder",
        props: {
            img: {
                type: String,
                default: '/static/images/placeholder.png',
            },
            title: String,
        },
        data() {
            return {}
        },

        components: {},

        methods: {},
    }
</script>

