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

        <img v-lazy="img" alt="">
        <p>
            说明：长按或右击证书图片下载。
        </p>
    </div>
</template>

<script>
    import {getAuthorization} from "src/api/api"

    export default {
        name: "authorization",

        data() {
            return {
                img: ''
            }
        },

        components: {},

        methods: {
            setAuthorization(){
                getAuthorization().then(
                    resData => {
                        if(resData){
                            this.img = resData.data.url;
                        }
                    }
                )
            }
        },

        created(){
            this.setAuthorization();
        }
    }
</script>

