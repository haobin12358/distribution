<style lang="less" scoped>
    @import "../../common/css/index";

    .common-layout {
        .fj();
        .wl(100vw, 100vh);

        .left-aside {
            .wl(2.6rem, 100vh);
            overflow-y: scroll;
            background: #545c64;

            .tac {
                .system-title{
                    text-align: center;
                    font-size: .26rem;
                    color: #d1dbe5;
                    padding: .12rem;
                    border-bottom: 1px dotted #d1dbe5;
                }
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
                    <p class="system-title">
                        蓓莉云仓后台管理系统
                    </p>
                    <el-menu class="m-sidebar" :default-active="defaultPage.path" background-color="#545c64"
                             text-color="#ffffff" active-text-color="#ffd04b" :router="true">
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
                    <!--开发版本:2018.11.27-->
                </span>
                <!--<el-input class="search-input" size="mini" v-model="searchTxt" placeholder="请输入内容"></el-input>-->
                <el-autocomplete prefix-icon="el-icon-menu" placeholder="请输入菜单名" v-model="searchTxt"
                                 value-key="title"  :fetch-suggestions="querySearch" @select="selectMenu">
                </el-autocomplete>
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

            menuList(){
                let menuList = [];

                for (let i = 0; i < this.menu.length; i++) {
                    let currentMenu = this.menu[i];

                    if(currentMenu.children){
                        for (let j = 0; j < currentMenu.children.length; j++) {
                            menuList.push({
                                title: currentMenu.children[j].title,
                                path:currentMenu.path + '/'+currentMenu.children[j].path
                            });

                        }
                    }else{
                        menuList.push(currentMenu);
                    }
                }

                return menuList;
            },

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

            },

            querySearch(queryString, cb) {
                // console.log(queryString);
                let searchRes =  this.menuList.filter(item => item.title .toLowerCase().indexOf(queryString.toLowerCase()) !== -1)

                cb(searchRes);
            },
            selectMenu(menu){
                console.log(menu);
                this.$router.push(menu.path)
            },

        },

        created() {
            // console.log(this.$route.path.split('/')[2]);
        },
    }
</script>

