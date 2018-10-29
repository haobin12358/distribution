<style lang="less" scoped>
    @import "../../common/css/index";

    .footer {
        z-index: 100;
        background: white;
        position: fixed;
        left: 0;
        bottom: 0;
        border-top: 1px solid #c1c1c1;
        padding: 21px 89px 0;
        box-sizing: border-box;
        .wl(100%, 92px);
        .fj();

        .footer-item {
            position: relative;
            .fj(center);
            flex-direction: column;

            &:nth-child(1) {
                .tab-icon {
                    .wl(59px, 43px);
                }
            }
            &:nth-child(2) {
                .tab-icon {
                    .wl(43px, 43px);
                }
            }
            &:nth-child(3) {
                .tab-icon {
                    .wl(40px, 43px);
                }
            }

            .tab-red-dot {
                position: absolute;
                right: 0;
                top: 0;
                transform: translate(50%, -50%);
                .wl(31px, 31px);
                background: red;
                border-radius: 31px;
                .fontc(34px);
                color: #ffffff;
                .fz(22px);

            }

            .tab-title {
                text-align: center;
                .sc(20px, #aeaeae);

                &.active {
                    color: @mainColor;
                }

            }
        }
    }

</style>

<template>
    <div class="footer">
        <section class="footer-item" @click="gotoAddress('/message')">
            <img class="tab-icon"
                 :src="$route.path.indexOf('message')!=-1?'/static/images/tabbar_message_active.png':'/static/images/tabbar_message.png'"
                 alt="">
            <span :class="{'tab-title': true,active: $route.path.indexOf('message')!=-1}">信息</span>

            <span class="tab-red-dot">{{notReadComMsgNum}}</span>
        </section>
        <section class="footer-item" @click="gotoAddress('/mall')">
            <img class="tab-icon"
                 :src="$route.path.indexOf('mall')!=-1?'/static/images/tabbar_home_active.png':'/static/images/tabbar_home.png'"
                 alt="">
            <span :class="{'tab-title': true,active: $route.path.indexOf('mall')!=-1}">云仓</span>
        </section>
        <section class="footer-item" @click="gotoAddress('/personal')">
            <img class="tab-icon"
                 :src="$route.path.indexOf('personal')!=-1 ? '/static/images/tabbar_person_active.png':'/static/images/tabbar_person.png'"
                 alt="">
            <span :class="{'tab-title': true,active: $route.path.indexOf('personal')!=-1}">我的</span>
        </section>
    </div>

</template>

<script>
    import {getStore} from "src/common/js/mUtils"
    import {NOT_READ_COM_MSGS} from "src/common/js/const"
    import {mapState} from "vuex"


    export default {
        name: "footerGuide",

        data() {
            return {
            }
        },

        computed:{
            ...mapState({
                notReadComMsgNum(state){
                    return state.notReadComMsg > getStore(NOT_READ_COM_MSGS) ?this.$store.state.notReadComMsg : getStore(NOT_READ_COM_MSGS);
                }
            })
        },

        components: {},

        methods: {
            gotoAddress(path) {
                this.$router.push(path);
            }
        },
    }
</script>

