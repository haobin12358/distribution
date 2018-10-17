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
                .fontc(36px);
                color: #ffffff;
                .fz(24px);

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

            <span class="tab-red-dot">8</span>
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
    export default {
        name: "footerGuide",

        data() {
            return {}
        },

        components: {},

        methods: {
            gotoAddress(path) {
                this.$router.push(path);
            }
        },
    }
</script>

