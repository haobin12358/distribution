<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();

        .form-container {
            margin-top: 10px;
            .bs(0, 3px, 6px);
            padding: 20px;
            .bgw();

        }
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <section class="form-container">
            <mt-field class="form-item" label="有效期限" placeholder="请选择有效期限" v-model="expiryDate" :readonly="true"
                      :disableClear="true" @click.native="sheetVisible =true"></mt-field>
            <mt-field class="form-item" label="可用次数" placeholder="请输入可用次数"></mt-field>


            <mt-field class="form-item" label="邀请人" placeholder="有就用默认地址的"></mt-field>
            <mt-field class="form-item" label="电话" placeholder="有就用默认地址的"></mt-field>
            <mt-field class="form-item" label="地址" placeholder="有就用默认地址的"></mt-field>
        </section>

        <section class="my-confirm-btn-wrap">
            <router-link to="/inviteLink" tag="button" class="my-confirm-btn">确 认</router-link>
        </section>

        <mt-actionsheet
            :actions="actions"
            v-model="sheetVisible">
        </mt-actionsheet>
    </div>
</template>

<script>
    export default {
        name: "newInvite",

        data() {
            return {
                expiryDate: '',

                actions: [
                    {name: '一天', method: this.selectExpiryDate},
                    {name: '三天', method: this.selectExpiryDate},
                    {name: '一星期', method: this.selectExpiryDate},
                ],
                sheetVisible: false,
            }
        },

        components: {},

        computed: {},

        methods: {
            selectExpiryDate(evt){
                this.expiryDate = evt.name;
            }
        },

        created() {
        },
    }
</script>

