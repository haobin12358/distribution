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

        <template v-if="(showAgent && agentMessages.length) || (!showAgent && companyMessages.length)">
            <ul v-show="showAgent" class="message-list">
                <li class="message-item" v-for="item in agentMessages">
                    <section class="item-hd">
                    <span class="title">
                         {{item.AMtypeCH}}
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
            <ul v-show="!showAgent" class="message-list">
                <li class="message-item" v-for="item in companyMessages" @click="gotoMessageDetail(item)">
                    <section class="item-hd">
                        <img v-if="item.isread == 0" class="message-new" src="/static/images/message_new.png" alt=""/>
                        <span class="title">公告</span>
                        <span class="date">{{item.CMdate}}</span>
                    </section>
                    <section class="item-bd">
                        {{item.CMtitle}}
                    </section>
                </li>
            </ul>
            <load-more :type="loadingType"></load-more>
        </template>
        <template v-else>
            <place-holder title="暂时没有该类消息"></place-holder>
        </template>

        <footer-guide></footer-guide>
    </div>
</template>

<script>
    import footerGuide from "src/components/footer/footerGuide"
    import LoadMore from "src/components/common/loadMore"
    import PlaceHolder from "src/components/common/placeHolder"
    import {mapState, mapMutations} from 'vuex'
    import {getAgentMessage, getCompanyMessage} from "src/api/api"
    import {setStore, getStore} from "src/common/js/mUtils"
    import {TOKEN, USER_INFO, AM_TYPE} from "src/common/js/const"
    import common from "src/common/js/common"

    export default {
        name: "message",

        data() {
            return {
                page: 1,    // 页数
                count: 10,  // 条数
                loadingType: 'normal',  // 加载组件加载状态

                agentMessages: [],
                companyMessages: [],
            }
        },

        computed: {
            ...mapState(['showAgent'])
        },

        components: {
            footerGuide,
            LoadMore,
            PlaceHolder,
        },

        methods: {
            ...mapMutations({
                setShowAgent: 'SET_SHOW_AGENT'
            }),
            getDataInit() {
                this.page = 1;

                if (this.showAgent) {
                    this.getAgentMessage(true);
                } else {
                    this.getCompanyMessage(true);
                }
            },
            // 滚动条监听事件
            touchMove() {
                let scrollTop = common.getScrollTop();
                let scrollHeight = common.getScrollHeight();
                let ClientHeight = common.getClientHeight();

                if (scrollTop + ClientHeight >= scrollHeight - 10 && this.loadingType == 'normal') {
                    if (this.showAgent) {
                        this.getAgentMessage();
                    } else {
                        this.getCompanyMessage();
                    }
                }
            },
            // 切换消息类型
            switchTab(bool) {
                this.setShowAgent(bool);
                this.getDataInit();
            },
            // 点击消息详情
            gotoMessageDetail(msg) {
                this.$router.push({path: '/messageDetail', query: msg});
            },

            /**
             * 获得代理消息
             * @param replace   替换 是否从第一页开始
             */
            getAgentMessage(replace) {
                this.loadingType = 'loading';

                getAgentMessage(this.page).then(
                    ({data: list}) => {
                        if (list.length < this.count) {
                            this.loadingType = 'nomore';
                        } else {
                            this.loadingType = 'normal';
                        }

                        if (list.length) {
                            for (let i = 0; i < list.length; i++) {
                                list[i].AMtypeCH =AM_TYPE[ list[i].AMtype];
                            }
                            if (!replace) {
                                this.agentMessages = [...this.agentMessages, ...list];
                            } else {
                                this.agentMessages = list;
                            }
                            this.page++;
                        }
                    }
                )
            },
            /**
             * 获得公司消息
             * @param replace   替换 是否从第一页开始
             */
            getCompanyMessage(replace) {
                this.loadingType = 'loading';

                getCompanyMessage(this.page).then(
                    ({data: list, notread}) => {
                        if (list.length < this.count) {
                            this.loadingType = 'nomore';
                        } else {
                            this.loadingType = 'normal';
                        }

                        this.$store.commit('SET_NOT_READ_COM_MSG', notread);

                        if (list.length) {
                            if (!replace) {
                                this.companyMessages = [...this.companyMessages, ...list];
                            } else {
                                this.companyMessages = list;
                            }

                            this.page++;
                        }
                    }
                )
            },
        },

        destroyed() {
            window.removeEventListener('scroll', this.touchMove);
        },

        mounted() {
            window.addEventListener('scroll', this.touchMove);
        },

        created() {
            this.getDataInit();
        }

    }
</script>

