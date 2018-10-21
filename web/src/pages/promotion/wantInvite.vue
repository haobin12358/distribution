<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .invite-code-list{
            margin-top: 10px;

            .invite-code-item{
                .bgw();
                .bs(10px, 3px, 6px);
                padding: 25px;
                .fj();

                .invite-code-img{
                    .wl(100px, 100px);
                    margin-right: 40px;
                }

                .invite-remain{
                    flex: 1;
                    display: flex;
                    justify-content: space-between;
                    flex-direction: column;

                    .deadline{
                    }
                }


                .remove-btn{
                    align-self: center;
                    .wl(40px, 40px);
                }
            }
        }
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true">
            <section slot="right">
                <router-link to="/newInvite" tag="img" src="/static/images/add.png"
                             class="my-add-img"></router-link>
            </section>
        </header-top>

        <ul class="invite-code-list">
            <li class="invite-code-item" v-for="item in 4">
                <img src="/static/images/testbg.jpg" alt="" class="invite-code-img">

                <section class="invite-remain">
                    <span class="deadline">有限期限：2018-08-15 14：56：24</span>
                    <span class="residue-degree">可用次数：10</span>
                </section>

                <img src="/static/images/close.png" alt="" class="remove-btn">
            </li>
        </ul>

    </div>
</template>

<script>
    export default {
        name: "wantInvite",

        data() {
            return {}
        },

        components: {},

        computed: {},

        methods: {},

        created() {
        },
    }
</script>

