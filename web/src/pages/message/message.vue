<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        min-height: 100vh;
        padding-top: 20px;
        padding-bottom: 100px;

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
                box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.16);
                background: white;

                .item-hd {
                    .fj();
                    padding-bottom: 11px;
                    border-bottom: 1px solid #DBDBDB;

                    .message-new {
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
            <section :class="{'tab-item': true,active: showAgent}" @click="switchTab(true)">代理消息</section>
            <section :class="{'tab-item': true,active: !showAgent}" @click="switchTab(false)">公司消息</section>
        </header>

        <scroll
            :data="agentMessages"
            :pulldown="true"
            @pulldown="$log('上拉刷新')">
            <ul v-if="showAgent" class="message-list">
                <li class="message-item" v-for="item in agentMessages" @click="gotoMessageDetail(item)">
                    <section class="item-hd">
                        <!--<img v-if="item.unread" class="message-new" src="/static/images/message_new.png" alt=""/>-->
                        <span class="title">
                      {{item.title}}
                    </span>
                        <span class="date">
                        {{item.AMdate}}
                  </span>
                    </section>
                    <section class="item-bd">
                        {{item.AMcontent}}
                    </section>
                </li>
            </ul>
        </scroll>

        <!--<ul v-else="!showAgent" class="message-list">-->
        <!--<li class="message-item" v-for="item in agentMessages" @click="gotoMessageDetail(item)">-->
        <!--<section class="item-hd">-->
        <!--&lt;!&ndash;<img v-if="item.unread" class="message-new" src="/static/images/message_new.png" alt=""/>&ndash;&gt;-->
        <!--<span class="title">-->
        <!--{{item.title}}-->
        <!--</span>-->
        <!--<span class="date">-->
        <!--{{item.AMdate}}-->
        <!--</span>-->
        <!--</section>-->
        <!--<section class="item-bd">-->
        <!--{{item.AMcontent}}-->
        <!--</section>-->
        <!--</li>-->
        <!--</ul>-->

        <footer-guide></footer-guide>
    </div>
</template>

<script>
    import scroll from "src/components/common/scroll"
    import footerGuide from "src/components/footer/footerGuide"
    import {mapState, mapMutations} from 'vuex'
    import {getAgentMessage, getCompanyMessage} from "src/api/api"
    import BSscroll from "better-scroll"
    import {setStore, getStore} from "src/common/js/mUtils"
    import {TOKEN, USER_INFO} from "src/common/js/const"

    export default {
        name: "message",

        data() {
            return {
                showAgent: true,
                page: 1,
                count: 10,

                agentMessages: [],
                companyMessages: [],

                scroll: {}
            }
        },

        components: {
            footerGuide,
            scroll
        },

        methods: {
            switchTab(bool) {
                this.showAgent = bool;
            },
            gotoMessageDetail(msg) {
                this.$router.push('/messageDetail')
            },
            getAgentMessage() {
                getAgentMessage(this.page).then(
                    data => {
                        if (data) {
                            if (data.length < this.count) {
                                console.log('没了');
                            } else {
                                console.log('可以加载第二页');
                            }

                            this.agentMessages = data;
                            if (this.page == 1) {
                                this.$nextTick(() => {
                                    // this.scroll = new BSscroll(this.$refs.wrapper, {});
                                });
                            }
                        }
                    }
                )
            }
        },

        mounted() {
            // this.$nextTick(() => {
            //     this.scroll = new BSscroll(this.$refs.wrapper, {});
            // });
        },

        created() {
            if (this.showAgent) {
                this.getAgentMessage();
            }

        }

    }
</script>

