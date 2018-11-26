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


            .menu-title{
                .fz(1rem);
            }
        }

        .right-content {
            flex: 1;
            padding-left: .2rem;
            padding-right: .4rem;
            overflow-y: scroll;
            /*overflow: scroll;*/
            .right-content-hd {
                height: 1rem;
                .fj(flex-end);
                align-items: center;
                /*border-bottom: 3px solid rgba(63, 63, 63, .3);*/

                .search-input {
                    width: 3rem;
                }

                .admin-name {
                    .fz(0.24rem);
                    margin: 0 .2rem 0 .5rem;
                    cursor: pointer;
                }

                .head-img {
                    .wl(.31rem, .34rem);
                }
            }

            .main-view {
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
                    <el-menu class="m-sidebar" :default-active="defaultPage.path" background-color="#545c64"
                             text-color="#fff" popper-class="menu-title" active-text-color="#ffd04b" :router="true">
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
                <span class="version">
                    开发版本:2018.11.26
                </span>
                <el-input class="search-input" size="mini" v-model="searchTxt" placeholder="请输入内容"></el-input>
                <el-dropdown class="admin-name" trigger="click" @command="handleCommand">
                    <span class="el-dropdown-link">
                        Admin
                      <i class="el-icon-arrow-down el-icon--right"></i>
                     </span>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item command="logout">退出系统</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
                <img class="head-img" src="/static/images/admin.png" alt="">
            </header>

            <main class="main-view">
                <el-tabs v-if="showTabPane" :value="secondIndex" @tab-click="handleClick">
                    <el-tab-pane v-for="item in defaultPage.children" :label="item.title"
                                 :name="item.path" :key="item.path">
                    </el-tab-pane>
                </el-tabs>
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

        components: {},

        computed: {
            ...mapState(['menu']),

            defaultIndex() {
                let firstLevelPath = '/' + this.$route.path.split('/')[1]

                return firstLevelPath;
            },
            secondIndex() {
                let secondLevelPath = this.$route.path.split('/')[2]

                return secondLevelPath;
            },


            defaultPage() {
                let firstLevelPath = '/' + this.$route.path.split('/')[1]

                return this.menu.find(menu => menu.path == firstLevelPath);
            },

            showTabPane() {
                let isSecond;

                if (this.defaultPage.children) {
                    isSecond = this.defaultPage.children.find(item => item.path == this.secondIndex);

                }

                return this.defaultPage.children && this.defaultPage.children.length && isSecond
            },
        },

        methods: {
            handleClick(tab) {
                this.$router.push(tab.name)
            },
            handleCommand(command){
                switch (command) {
                    case 'logout':
                        this.$common.setStore('token', '');
                        this.$router.push('/login');
                        break;
                }

            }
        },

        created() {
            // console.log(this.$route.path.split('/')[2]);
        },
    }
</script>

