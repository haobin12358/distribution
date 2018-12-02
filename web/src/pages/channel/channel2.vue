<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();
        .bgw();

        .channel-list{
            .channel-item{
                .fj();
                align-items: center;
                padding: 20px 20px 20px 0;
                border-top: 2px solid @grayBorderColor;

                &:last-child{
                    border-bottom: 2px solid @grayBorderColor;

                }

                .channel-item-bd{
                    flex: 1;
                    .fj(flex-start);
                    /*align-items: center;*/

                    .head-img{
                        .wl(100px, 100px);
                        border: 2px solid @mainColor;
                        border-radius: 50%;
                        margin-right: 80px;
                    }

                    .info-wrap{
                        .fjc();
                        padding: 10px 0;
                        /*height: 0px;*/

                    }
                }

                .channel-item-ft-arrow{
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
            <li v-for="item,index in channelType" :class="{'nav-bar-item': true, 'active': selectedChannelIndex == index}"
                @click="selectedChannelIndex = index">
                {{item.label}}({{item.num || 0}})
            </li>
        </ul>

        <ul class="channel-list">
            <li v-for="item in showList" class="channel-item">
                <section class="channel-item-bd">
                    <img :src="item.USheadimg" alt="" class="head-img"/>

                    <section class="info-wrap">
                        <p>姓名:{{item.USname}}</p>
                        <p>代理编号:{{item.USagentid}}</p>
                    </section>
                </section>
                <img src="/static/images/arrow.png" class="channel-item-ft-arrow"/>
            </li>
        </ul>

        <place-holder v-show="!showList.length" title="渠道列表为空"></place-holder>
    </div>
</template>

<script>
    import {getDirectagent, getDistribute} from "src/api/api"
    import pinyin from "pinyin"
    import PlaceHolder from "src/components/common/placeHolder"

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
                    },{
                        label: '分销商',
                        num: 0,
                    },
                ],

                directAgent: [],
                distribute: [],
            }
        },

        computed: {
            showList(){
                if(this.selectedChannelIndex == 0){
                    return this.directAgent;
                }else{
                    return this.distribute;
                }
            }
        },

        methods: {
            switchOrderType(index){
                this.selectedChannelIndex = index;
            },

            setData(){
                getDirectagent().then(
                    resData => {
                        if(resData){
                            let data = resData.data;

                            this.directAgent = data;
                            this.channelType[0].num = resData.directcount;
                            this.channelType[1].num = resData.distribucount;
                        }
                    }
                );

                getDistribute().then(
                    resData => {
                        if(resData){
                            let data = resData.data;

                            this.distribute = data;
                        }
                    }
                );


            },
        },

        created() {
            this.setData();
        },
    }
</script>

