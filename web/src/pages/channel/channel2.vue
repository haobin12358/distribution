<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();

        .channel-list {
            .channel-item {
                .fj();
                align-items: center;
                padding: 20px 20px 20px 10px;
                border-top: 2px solid @grayBorderColor;
                .bgw();

                &:last-child {
                    border-bottom: 2px solid @grayBorderColor;

                }

                .channel-item-bd {
                    flex: 1;
                    .fj(flex-start);
                    /*align-items: center;*/

                    .head-img {
                        .wl(100px, 100px);
                        border: 2px solid @mainColor;
                        border-radius: 50%;
                        margin-right: 80px;
                    }

                    .info-wrap {
                        .fjc();
                        padding: 10px 0;
                        /*height: 0px;*/

                    }
                }

                .channel-item-ft-arrow {
                    .wl(40px, 80px);
                }
            }
        }
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>

        <ul class="nav-bar">
            <li v-for="item,index in channelType"
                :class="{'nav-bar-item': true, 'active': selectedChannelIndex == index}"
                @click="switchChannelType(index)">
                {{item.label}}({{item.num || 0}})
            </li>
        </ul>

        <template v-if="showList.length">
            <ul class="channel-list">
                <li v-for="item in showList" class="channel-item">
                    <section class="channel-item-bd">
                        <img v-lazy="item.USheadimg" alt="" class="head-img"/>

                        <section class="info-wrap">
                            <p>姓名:{{item.USname}}</p>
                            <p>代理编号:{{item.USagentid}}</p>
                        </section>
                    </section>
                    <img src="/static/images/arrow.png" class="channel-item-ft-arrow"/>
                </li>
            </ul>
            <load-more :type="loadingType"></load-more>
        </template>

        <place-holder v-else title="渠道列表为空"></place-holder>
    </div>
</template>

<script>
    import {getDirectagent, getDistribute} from "src/api/api"
    import PlaceHolder from "src/components/common/placeHolder"
    import common from "src/common/js/common"

    export default {
        name: "channel2",

        components: {
            PlaceHolder
        },

        data() {
            return {
                selectedChannelIndex: 0,
                channelType: [
                    {
                        label: '直属代理',
                        num: 0,
                    }, {
                        label: '分销商',
                        num: 0,
                    },
                ],

                page: 1,    // 页数
                count: 10,  // 条数
                loadingType: 'normal',  // 加载组件加载状态

                directAgent: [],
                distribute: [],
            }
        },

        computed: {
            showList() {
                if (this.selectedChannelIndex == 0) {
                    return this.directAgent;
                } else {
                    return this.distribute;
                }
            }
        },

        methods: {
            switchChannelType(index) {
                this.selectedChannelIndex = index;
                console.log(this.selectedChannelIndex);
                this.setInitData();
                return
            },

            setInitData() {
                this.page = 1;

                if (this.selectedChannelIndex) {
                    this.setDistribute(true);
                } else {
                    this.setDirectagent(true);
                }
            },

            // 滚动条监听事件
            touchMove() {
                let scrollTop = common.getScrollTop();
                let scrollHeight = common.getScrollHeight();
                let ClientHeight = common.getClientHeight();

                if (scrollTop + ClientHeight >= scrollHeight - 10 && this.loadingType == 'normal') {
                    if (this.selectedChannelIndex) {
                        this.setDistribute();
                    } else {
                        this.setDirectagent();
                    }
                }
            },

            setDirectagent(replace) {
                this.loadingType = 'loading';

                getDirectagent(this.page).then(
                    resData => {
                        if (resData) {
                            let data = resData.data;

                            if (data.length < this.count) {
                                this.loadingType = 'nomore';
                            } else {
                                this.loadingType = 'normal';
                            }

                            if (data.length) {
                                if (!replace) {
                                    this.directAgent = [...this.directAgent, ...data];
                                } else {
                                    this.directAgent = data;
                                }
                                this.page++;
                            }

                            this.channelType[0].num = resData.directcount;
                            this.channelType[1].num = resData.distribucount;
                        }
                    }
                )
            },
            setDistribute(replace) {
                this.loadingType = 'loading';

                getDistribute(this.page).then(
                    resData => {
                        if (resData) {
                            let data = resData.data;

                            if (data.length < this.count) {
                                this.loadingType = 'nomore';
                            } else {
                                this.loadingType = 'normal';
                            }

                            if (data.length) {
                                if (!replace) {
                                    this.distribute = [...this.distribute, ...data];
                                } else {
                                    this.distribute = data;
                                }
                                this.page++;
                            }
                        }
                    }
                )
            },
        },

        destroyed(){
            window.removeEventListener('scroll', this.touchMove);

        },

        mounted(){
            window.addEventListener('scroll', this.touchMove);

        },



        created() {
            this.setInitData();
        },
    }
</script>

