<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        //.least-full-screen();
        .bgw();

        .search-bar-wrap {
            padding: 15px 25px;
            background: #eeeeee;

            .search-bar {
                .wl(694px, 50px);
                .bgw();
                border-radius: 50px;
                padding: 0 20px;
                box-sizing: border-box;
                .fj(flex-start);
                align-items: center;

                .icon {
                    .wl(30px, 30px);
                    margin-right: 30px;
                }

                input {
                    flex: 1;
                    height: 100%;
                    .sc(24px, #999999);
                }

                .close {
                    .wl(48px, 48px);

                }
            }
        }
        .people-info-item-wrap {
            padding-left: 33px;
            .bgw();

            .people-info-item {
                padding: 20px 0;
                .fj(flex-start);
                align-items: center;

                &:last-of-type {
                    border-bottom: none;
                }

                .people-img {
                    .wl(60px, 60px);
                    margin-right: 34px;
                }

                .people-name {
                    color: black;
                    margin-right: 30px;

                }

                .people-phone {
                    color: #999999;

                }
            }
        }

    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true"></header-top>
        <mt-navbar v-model="selected" style="margin-bottom: 3px">
            <mt-tab-item id="1">直属代理 ({{directAgentLen}})</mt-tab-item>
            <mt-tab-item id="2">分销商 ({{distributeAgentLen}})</mt-tab-item>
        </mt-navbar>

        <section class="search-bar-wrap">
            <section class="search-bar">
                <img src="/static/images/search.png" class="icon" alt="">
                <input type="text" placeholder="搜索联系人" v-model="addressBookSearch">
                <transition name="router-fade">
                    <img v-if="addressBookSearch" src="/static/images/close.png" class="icon"
                         @click="addressBookSearch = ''" alt="">
                </transition>
            </section>
        </section>

        <mt-tab-container v-model="selected" :swipeable="true">
            <mt-tab-container-item id="1">
                <mt-index-list v-if="directAgentFilter.length">
                    <mt-index-section v-for="indexItem in directAgentFilter" :key="indexItem.index"
                                      :index="indexItem.index">
                        <section class="people-info-item-wrap">
                            <section class="people-info-item" v-for="info in indexItem.list">
                                <img :src="info.USheadimg" alt="" class="people-img">

                                <span class="people-name">{{info.USname}}</span>
                                <span class="people-phone">{{info.USagentid}}</span>
                            </section>
                        </section>
                    </mt-index-section>
                </mt-index-list>
                <place-holder1 v-else title="你还没有直属代理"></place-holder1>

            </mt-tab-container-item>
            <mt-tab-container-item id="2">
                <mt-index-list v-if="distributeAgentFilter.length">
                    <mt-index-section v-for="indexItem in distributeAgentFilter" :key="indexItem.index"
                                      :index="indexItem.index">
                        <section class="people-info-item-wrap">
                            <section class="people-info-item" v-for="info in indexItem.list">
                                <img :src="info.USheadimg" alt="" class="people-img">
                                <span class="people-name">{{info.USname}}</span>
                                <span class="people-phone">{{info.USagentid}}</span>
                            </section>
                        </section>
                    </mt-index-section>
                </mt-index-list>
                <place-holder2 v-else title="你还没有分销商"></place-holder2>

            </mt-tab-container-item>
        </mt-tab-container>
    </div>
</template>

<script>
    import {getDirectagent, getDistribute} from "src/api/api"
    import pinyin from "pinyin"
    import PlaceHolder from "src/components/common/placeHolder"

    const addressBookIndexes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '#'];

    export default {
        name: "channel",

        data() {
            return {
                selected: '1',

                addressBookSearch: '',

                directAgent: [],    //  直属代理
                distributeAgent: [],    //  分销商

                directAgentLen: 0,
                distributeAgentLen: 0,

            }
        },


        computed: {
            directAgentFilter() {
                let rst = [];



                if (!this.addressBookSearch) {
                    return this.directAgent;
                }

                for (let i = 0; i < this.directAgent.length; i++) {
                    let matchPeople = [],
                        currentPeopleIndex = this.directAgent[i];

                    for (let j = 0; j < currentPeopleIndex.list.length; j++) {
                        let currentPeople = currentPeopleIndex.list[j];

                        if (currentPeople.USname.toUpperCase().indexOf(this.addressBookSearch.toUpperCase()) != -1 || currentPeople.USagentid.toString().indexOf(this.addressBookSearch) != -1) {
                            matchPeople.push(currentPeople);
                        }
                    }

                    if (matchPeople.length) {
                        rst.push({
                            index: currentPeopleIndex.index,
                            list: matchPeople
                        });
                    }
                }

                return rst;
            },
            distributeAgentFilter() {
                let rst = [];

                if (!this.addressBookSearch) {
                    return this.distributeAgent;
                }

                for (let i = 0; i < this.distributeAgent.length; i++) {
                    let matchPeople = [],
                        currentPeopleIndex = this.distributeAgent[i];

                    for (let j = 0; j < currentPeopleIndex.list.length; j++) {
                        let currentPeople = currentPeopleIndex.list[j];

                        if (currentPeople.USname.toUpperCase().indexOf(this.addressBookSearch.toUpperCase()) != -1 || currentPeople.USagentid.toString().indexOf(this.addressBookSearch) != -1) {
                            matchPeople.push(currentPeople);
                        }
                    }

                    if (matchPeople.length) {
                        rst.push({
                            index: currentPeopleIndex.index,
                            list: matchPeople
                        });
                    }
                }

                return rst;
            },


        },

        components: {
            PlaceHolder1: PlaceHolder,
            PlaceHolder2: PlaceHolder,
        },

        methods: {
            getWordFirstLetter(word) {
                let rst = pinyin(word[0], {
                    style: pinyin.STYLE_FIRST_LETTER
                })[0][0].toUpperCase();

                if (rst.match(/\d/)) {
                    rst = '#'
                }

                return rst;
            },
            //  处理成联系人列表格式
            dataToAddressList(data) {
                let rst = [];

                for (let i = 0; i < addressBookIndexes.length; i++) {
                    rst.push({
                        index:addressBookIndexes[i],
                        list: []
                    })
                }

                for (let i = 0; i < data.length; i++) {
                    let groupIndex = 0,
                        exist = rst.some((group, index) => {
                            groupIndex = index;
                            return group.index == this.getWordFirstLetter(data[i].USname);
                        });

                    rst[groupIndex].list.push(
                        data[i]
                    );
                }

                rst = rst.filter(item => item.list.length)

                return rst;
            },
            //
            setData() {
                getDirectagent().then(
                    resData => {
                        if (resData) {
                            this.directAgent = this.dataToAddressList(resData.data);
                            this.directAgentLen = resData.directcount
                            this.distributeAgentLen = resData.distribucount
                        }
                    }
                );
                getDistribute().then(
                    resData => {
                        if (resData) {
                            this.distributeAgent = this.dataToAddressList(resData.data);
                        }
                    }
                );
            }
        },

        created() {
            // this.dataToAddressList();
            this.setData();

            // console.log(pinyin('a'));
            // console.log(pinyin('1'));
        }
    }
</script>

