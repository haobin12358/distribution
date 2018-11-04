<style lang="less" scoped>
    @import "../../common/css/index";

    .common-layout {
        .fj();
        .wl(100vw, 100vh);

        .left-aside {
            .wl(4rem, 100vh);
            overflow-y: scroll;
            background: #545c64;

            .tac {
            }
        }

        .right-content{
            flex: 1;
            padding-left: .2rem;
            padding-right: .4rem;
            overflow-y: scroll;
            /*overflow: scroll;*/
            .right-content-hd{
                height: 1rem;
                .fj(flex-end);
                align-items: center;
                /*border-bottom: 3px solid rgba(63, 63, 63, .3);*/

                .search-input{
                    width: 3rem;
                }

                .admin-name{
                    .fz(0.24rem);
                    margin:  0 .2rem 0 .5rem;
                }

                .head-img{
                    .wl(.31rem, .34rem);
                }
            }

            .main-view{
                padding-bottom: 1rem;
            }
        }
    }
</style>

<template>
    <div class="common-layout">
        <aside class="left-aside">
            <el-row class="tac">
                <el-col :span="24">
                    <el-menu :default-active="defaultIndex" class="el-menu-vertical-demo" background-color="#545c64" text-color="#fff"
                        active-text-color="#ffd04b" :router="true">
                        <el-menu-item v-for="item,index in menu" :index="item.path" :key="index">
                            <i class="el-icon-menu"></i>
                            <span slot="title">{{item.title}}</span>
                        </el-menu-item>
                    </el-menu>
                </el-col>
            </el-row>
        </aside>

        <section class="right-content">
            <header class="right-content-hd">
                <el-input class="search-input" size="mini" v-model="searchTxt" placeholder="请输入内容"></el-input>
                <span class="admin-name">Admin</span>
                <img class="head-img" src="/static/images/admin.png" alt="">
            </header>

            <main class="main-view">
                <router-view>

                </router-view>
            </main>
        </section>
    </div>
</template>

<script>
    import {mapState} from "vuex"

    export default {
        name: "commonLayout",

        data() {
            return {
                searchTxt: ''
            }
        },

        components: {
        },

        computed: {
            ...mapState(['menu']),

            defaultIndex(){
                let firstLevelPath ='/'+ this.$route.path.split('/')[1]

                return firstLevelPath;
            }
        },

        methods: {
            // handlerSelect(index, key) {
            //     if ()
            //     this.$route.push(index);
            // }
        },

        created() {
        },
    }
</script>

