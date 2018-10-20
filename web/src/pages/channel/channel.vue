<style lang="less" scoped>
    @import "../../common/css/index";

    .container {

        .search-bar-wrap {
            padding: 15px 25px;

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

                .close{
                    .wl(48px, 48px);

                }
            }
        }
        .people-info-item-wrap {
            padding-left:33px ;
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
            <mt-tab-item id="1">直属代理 (20)</mt-tab-item>
            <mt-tab-item id="2">分销商 (21)</mt-tab-item>
        </mt-navbar>

        <section class="search-bar-wrap">
            <section class="search-bar">
                <img src="/static/images/search.png" class="icon" alt="">
                <input type="text" placeholder="搜索联系人" v-model="addressBookSearch">
                <transition name="router-fade">
                    <img v-if="addressBookSearch" src="/static/images/close.png" class="icon" @click="addressBookSearch = ''" alt="">
                </transition>
            </section>
        </section>

        <mt-tab-container v-model="selected" :swipeable="true">
            <mt-tab-container-item id="1">
                <section class="address-book">

                </section>
            </mt-tab-container-item>
            <mt-tab-container-item id="2">
            </mt-tab-container-item>
        </mt-tab-container>

        <mt-index-list>
            <mt-index-section v-for="indexItem in peopleListFilter" :key="indexItem.index" :index="indexItem.index">
                <section class="people-info-item-wrap">
                    <section class="people-info-item" v-for="info in indexItem.list">
                        <img src="/static/images/testbg.jpg" alt="" class="people-img">

                        <span class="people-name">{{info.name}}</span>
                        <span class="people-phone">{{info.phone}}</span>
                    </section>
                </section>


            </mt-index-section>
        </mt-index-list>
    </div>
</template>

<script>
    export default {
        name: "channel",

        data() {
            return {
                selected: '1',

                addressBookSearch: '',

                customerList: [
                    {
                        index: 'A',
                        list: [
                            {
                                name: 'A代理1',
                                phone: '123456'
                            }, {
                                name: 'A代理2',
                                phone: '123456'
                            }, {
                                name: 'A代理1',
                                phone: '123456'
                            }, {
                                name: 'A代理2',
                                phone: '123456'
                            }, {
                                name: 'A代理1',
                                phone: '123456'
                            }, {
                                name: 'A代理2',
                                phone: '123456'
                            }, {
                                name: 'A代理1',
                                phone: '123456'
                            }, {
                                name: 'A代理2',
                                phone: '123456'
                            }, {
                                name: 'A代理1',
                                phone: '123456'
                            }, {
                                name: 'A代理2',
                                phone: '123456'
                            },
                        ]
                    }, {
                        index: 'B',
                        list: [
                            {
                                name: 'B代理1',
                                phone: '123456'
                            }, {
                                name: 'B代理2',
                                phone: '123456'
                            }, {
                                name: 'B代理3',
                                phone: '123456'
                            }, {
                                name: 'B代理2',
                                phone: '123456'
                            }, {
                                name: 'B代理3',
                                phone: '123456'
                            },
                        ]
                    }, {
                        index: 'C',
                        list: [
                            {
                                name: 'C代理1',
                                phone: '123456'
                            },
                        ]
                    },
                ],

                addressBookIndexes: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '#'],
            }
        },


        computed: {
            peopleListFilter() {
                let rst = [];

                if (!this.addressBookSearch) {
                    return this.customerList;
                }

                for (let i = 0; i < this.customerList.length; i++) {
                    let matchPeople = [],
                        currentPeopleIndex = this.customerList[i];

                    for (let j = 0; j < currentPeopleIndex.list.length; j++) {
                        let currentPeople = currentPeopleIndex.list[j];

                        if (currentPeople.name.toUpperCase().indexOf(this.addressBookSearch.toUpperCase()) != -1 || currentPeople.phone.indexOf(this.addressBookSearch) != -1) {
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
            }

        },

        components: {},

        methods: {},
    }
</script>

