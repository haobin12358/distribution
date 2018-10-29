<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();

        .form-wrap{
            margin-top: 10px;
        }


    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <section class="form-wrap">
            <mt-field label="原密码" type="password" v-model="oldPassword" placeholder="请输入原密码"></mt-field>
            <mt-field label="新密码" type="password" v-model="newPassword" placeholder="请输入新密码"></mt-field>
            <mt-field label="新密码确认" type="password" v-model="newPasswordConfirm" placeholder="请再次输入新密码"></mt-field>
        </section>

        <section class="my-confirm-btn-wrap">
            <button class="my-confirm-btn" @click="doConfirmChange">确认</button>
        </section>
    </div>
</template>

<script>
    import {updatePwd} from "src/api/api"
    import {setStore} from "src/common/js/mUtils"

    export default {
        name: "changePassword",

        data() {
            return {
                oldPassword: '',
                newPassword: '',
                newPasswordConfirm: '',
            }
        },

        components: {},

        computed: {},

        methods: {
            formDataCheck(){
                if(!this.oldPassword){
                    return '请输入原密码!'
                }
                if(!this.newPassword){
                    return '请输入新密码!'
                }
                if(!this.newPasswordConfirm){
                    return '请再次输入新密码!'
                }

                if(this.newPasswordConfirm != this.newPassword){
                    return '请保证两次新密码输入一致!'
                }
            },
            doConfirmChange(){
                let checkMsg = this.formDataCheck();

                if(checkMsg){
                    this.$toast(checkMsg);
                }else{
                    updatePwd(this.oldPassword, this.newPassword).then(
                        (data)=>{
                            console.log(data);
                        }
                    )
                }
            },
        },

        created() {

        },
    }
</script>

