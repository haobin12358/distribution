<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        min-height: 100vh;
        padding-top: 20px;

        .container-hd {
            margin: 0 auto 20px;
            width: 350px;
            height: 40px;
            border-radius: 30px;
            background: @mainLightColor;

            .fj();

            .tab-item {
                flex: 1;
                .fontc(40px);
                border-radius: 30px;
                .sc(24px, white);

                &.active {
                    background: @mainColor;
                }
            }
        }

        .message-list {

            .message-item {
                padding: 30px 20px 40px;
                margin-bottom: 10px;
                box-shadow: 0px 3px 3px rgba(0, 0, 0, 0.16);
                background: white;

                .item-hd {
                    .fj();
                    padding-bottom: 11px;
                    border-bottom: 1px solid #DBDBDB;

                    .message-new{
                        .wl(38px, 38px);
                        margin-right: 10px;
                    }

                    .title {
                        flex: 1;
                        .fz(28px);
                    }
                    .date {
                        .fz(18px);
                    }
                }

                .item-bd {
                    padding-top: 11px;

                }

            }
        }
    }
</style>

<template>
    <div class="container">
        <header class="container-hd">
            <section :class="{'tab-item': true,active: showDaiLi}" @click="switchTab(true)">代理消息</section>
            <section :class="{'tab-item': true,active: !showDaiLi}" @click="switchTab(false)">公司消息</section>
        </header>
        <ul class="message-list" >
            <li class="message-item" v-for="item in messages" @click="gotoMessageDetail(item)">
                <section class="item-hd">
                    <img v-if="item.unread" class="message-new" src="/static/images/message_new.png" alt=""/>
                    <span class="title">
                      {{item.title}}
                  </span>
                    <span class="date">
                        {{item.date}}
                  </span>
                </section>
                <section class="item-bd">
                    {{item.content}}
                </section>
            </li>
        </ul>
        <footer-guide></footer-guide>

        <transition name="router-slid" mode="out-in">
            <router-view></router-view>
        </transition>
    </div>
</template>

<script>
    import footerGuide from "src/components/footer/footerGuide"
    import {mapState, mapMutations} from 'vuex'

    export default {
        name: "message",

        data() {
            return {
                showDaiLi: true,

                messages: [
                    {
                        title: '公告',
                        date: '2017-08-07 10:00:00',
                        content: '订单编号：01245846512313245645641',
                        unread: true,
                    }, {
                        title: '公告',
                        date: '2017-08-07 10:00:00',
                        content: '订单编号：01245846512313245645641',
                    }, {
                        title: '公告',
                        date: '2017-08-07 10:00:00',
                        content: '订单编号：01245846512313245645641',
                        unread: true,
                    }, {
                        title: '公告',
                        date: '2017-08-07 10:00:00',
                        content: '订单编号：01245846512313245645641',
                    },
                ]
            }
        },

        components: {
            footerGuide
        },

        methods: {
            ...mapMutations(['SAVE_READING_MESSAGE']),
            switchTab(bool) {
                this.showDaiLi = bool;
            },
            gotoMessageDetail(msg){
                this.$store.commit('SAVE_READING_MESSAGE',msg);
                this.$router.push('/message/messageDetail')
            }
        },
    }
</script>

