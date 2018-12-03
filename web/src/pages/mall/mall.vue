<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        padding-top: 80px;
        padding-bottom: 120px;
        .least-full-screen();

        #go-order-img {
            .wl(33px, 27px);
        }

        .pay-order {
            width: 129px;
            height: 46px;
            border: 2px solid rgba(255, 255, 255, 1);
            border-radius: 20px;
            .fontc(46px);
            .sc(26px, white);
            background: @mainColor;
        }

        .search-bar-wrap {
            padding: 15px 25px;
            background: #eeeeee;
            position: fixed;
            left: 0;
            top: 80px;
            width: 100%;

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

        .banner {
            height: 180px;
            margin-bottom: 10px;

            img {
                width: 100%;
                height: 100%;
            }
        }

        .nav-wrap {
            .nav-list-parent {
                background: white;
                overflow-x: scroll;
                white-space: nowrap;

                &.none {
                    height: 80px;

                }

                .nav-item {
                    height: 80px;
                    display: inline-block;
                    padding: 0 50px;
                    .fontc(80px);
                    box-sizing: border-box;

                    &.active {
                        color: @mainColor;
                        border-bottom: 3px solid @mainColor;
                    }
                }
            }
            .nav-list-children {
                height: 80px;
                overflow-x: scroll;
                .fj(flex-start);
                align-items: center;
                flex-wrap: nowrap;

                .pillow-item {
                    margin-right: 50px;
                    border: 1px solid rgba(110, 171, 184, 1);
                    border-radius: 30px;
                    white-space: nowrap;
                    /*height: 40px;*/
                    line-height: normal;
                    padding: 8px 40px;

                    &.active {
                        color: white;
                        background: @mainColor;
                    }

                    &:first-of-type {
                        margin-left: 42px;
                    }
                    &:last-of-type {
                        margin-right: 42px;
                    }
                }

                .pillow-item-tail {
                    flex: 42px;
                    .wl(42px, 10px);
                }

            }
        }

        .goods-list {
            padding: 0 10px;
            background: white;

            .goods-item {
                padding: 25px 2px 22px 16px;
                border-bottom: 2px solid #DBDBDB;
                .fj();

                &:last-child {
                    border-bottom: 0;
                }

                .goods-img {
                    margin-right: 40px;
                    .wl(120px, 120px);

                    img {
                        .wl(100%, 100%);
                    }
                }

                .goods-description {
                    flex: 1;
                    .fj();
                    flex-direction: column;
                    .goods-description-header {
                        .fj();
                        align-items: center;

                        .name {
                            .fz(28px);
                        }

                        .stock {
                            .sc(28px, @mainFontColor);
                            text-align: right;
                            margin-bottom: 10px;
                        }
                    }

                    .goods-description-content {
                        .fj();
                        align-items: center;

                        .goods-description-price {
                            .fz(28px);

                            .current-price {
                                margin-right: 20px;
                                color: #FC0000;

                            }
                            .original-price {
                                text-decoration: line-through;
                                color: @999;
                            }
                        }

                        .addToCartBtn {
                            padding: 10px 20px;
                            background: @mainColor;
                            .sc(24px, white);
                            border-radius: 30px;
                        }

                    }
                }
            }
        }

        .label-parent {
            .fj();
            align-items: center;
            text-align: center;
            border: 1px solid black;

            .label {

            }
        }

        .info {
            display: flex;
            align-items: center;
            padding: 0px;
            background: #db4000;
        }

        .zhiwei {
            /*width: 30px;*/
            border-radius: 30px;
            text-align: center;
            color: #FFFFFF;
            line-height: 24px;
            height: 24px;
            font-size: 24px;
            margin-left: 5px;
            white-space: nowrap;

        }

        .pay-order-fixed {
            position: fixed;
            left: 30px;
            bottom: 150px;
            .wl(120px, 120px);
            .fontc(40px);
            .fz(28px);
            border-radius: 50%;
            color: white;
        }
    }

    /*
    image[lazy=loading] {
        margin: 0 5px;
        .wl(40px, 40px);
        display: inline-block;
        vertical-align: middle;
        animation: myLoading 1s steps(12, end) infinite;
        background: transparent url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjAiIGhlaWdodD0iMTIwIiB2aWV3Qm94PSIwIDAgMTAwIDEwMCI+PHBhdGggZmlsbD0ibm9uZSIgZD0iTTAgMGgxMDB2MTAwSDB6Ii8+PHJlY3Qgd2lkdGg9IjciIGhlaWdodD0iMjAiIHg9IjQ2LjUiIHk9IjQwIiBmaWxsPSIjRTlFOUU5IiByeD0iNSIgcnk9IjUiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgLTMwKSIvPjxyZWN0IHdpZHRoPSI3IiBoZWlnaHQ9IjIwIiB4PSI0Ni41IiB5PSI0MCIgZmlsbD0iIzk4OTY5NyIgcng9IjUiIHJ5PSI1IiB0cmFuc2Zvcm09InJvdGF0ZSgzMCAxMDUuOTggNjUpIi8+PHJlY3Qgd2lkdGg9IjciIGhlaWdodD0iMjAiIHg9IjQ2LjUiIHk9IjQwIiBmaWxsPSIjOUI5OTlBIiByeD0iNSIgcnk9IjUiIHRyYW5zZm9ybT0icm90YXRlKDYwIDc1Ljk4IDY1KSIvPjxyZWN0IHdpZHRoPSI3IiBoZWlnaHQ9IjIwIiB4PSI0Ni41IiB5PSI0MCIgZmlsbD0iI0EzQTFBMiIgcng9IjUiIHJ5PSI1IiB0cmFuc2Zvcm09InJvdGF0ZSg5MCA2NSA2NSkiLz48cmVjdCB3aWR0aD0iNyIgaGVpZ2h0PSIyMCIgeD0iNDYuNSIgeT0iNDAiIGZpbGw9IiNBQkE5QUEiIHJ4PSI1IiByeT0iNSIgdHJhbnNmb3JtPSJyb3RhdGUoMTIwIDU4LjY2IDY1KSIvPjxyZWN0IHdpZHRoPSI3IiBoZWlnaHQ9IjIwIiB4PSI0Ni41IiB5PSI0MCIgZmlsbD0iI0IyQjJCMiIgcng9IjUiIHJ5PSI1IiB0cmFuc2Zvcm09InJvdGF0ZSgxNTAgNTQuMDIgNjUpIi8+PHJlY3Qgd2lkdGg9IjciIGhlaWdodD0iMjAiIHg9IjQ2LjUiIHk9IjQwIiBmaWxsPSIjQkFCOEI5IiByeD0iNSIgcnk9IjUiIHRyYW5zZm9ybT0icm90YXRlKDE4MCA1MCA2NSkiLz48cmVjdCB3aWR0aD0iNyIgaGVpZ2h0PSIyMCIgeD0iNDYuNSIgeT0iNDAiIGZpbGw9IiNDMkMwQzEiIHJ4PSI1IiByeT0iNSIgdHJhbnNmb3JtPSJyb3RhdGUoLTE1MCA0NS45OCA2NSkiLz48cmVjdCB3aWR0aD0iNyIgaGVpZ2h0PSIyMCIgeD0iNDYuNSIgeT0iNDAiIGZpbGw9IiNDQkNCQ0IiIHJ4PSI1IiByeT0iNSIgdHJhbnNmb3JtPSJyb3RhdGUoLTEyMCA0MS4zNCA2NSkiLz48cmVjdCB3aWR0aD0iNyIgaGVpZ2h0PSIyMCIgeD0iNDYuNSIgeT0iNDAiIGZpbGw9IiNEMkQyRDIiIHJ4PSI1IiByeT0iNSIgdHJhbnNmb3JtPSJyb3RhdGUoLTkwIDM1IDY1KSIvPjxyZWN0IHdpZHRoPSI3IiBoZWlnaHQ9IjIwIiB4PSI0Ni41IiB5PSI0MCIgZmlsbD0iI0RBREFEQSIgcng9IjUiIHJ5PSI1IiB0cmFuc2Zvcm09InJvdGF0ZSgtNjAgMjQuMDIgNjUpIi8+PHJlY3Qgd2lkdGg9IjciIGhlaWdodD0iMjAiIHg9IjQ2LjUiIHk9IjQwIiBmaWxsPSIjRTJFMkUyIiByeD0iNSIgcnk9IjUiIHRyYW5zZm9ybT0icm90YXRlKC0zMCAtNS45OCA2NSkiLz48L3N2Zz4=) no-repeat;
        background-size: 100%;

        &.weui-loading_transparent {
            background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 100 100'%3E%3Cpath fill='none' d='M0 0h100v100H0z'/%3E%3Crect xmlns='http://www.w3.org/2000/svg' width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.56)' rx='5' ry='5' transform='translate(0 -30)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.5)' rx='5' ry='5' transform='rotate(30 105.98 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.43)' rx='5' ry='5' transform='rotate(60 75.98 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.38)' rx='5' ry='5' transform='rotate(90 65 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.32)' rx='5' ry='5' transform='rotate(120 58.66 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.28)' rx='5' ry='5' transform='rotate(150 54.02 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.25)' rx='5' ry='5' transform='rotate(180 50 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.2)' rx='5' ry='5' transform='rotate(-150 45.98 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.17)' rx='5' ry='5' transform='rotate(-120 41.34 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.14)' rx='5' ry='5' transform='rotate(-90 35 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.1)' rx='5' ry='5' transform='rotate(-60 24.02 65)'/%3E%3Crect width='7' height='20' x='46.5' y='40' fill='rgba(255,255,255,.03)' rx='5' ry='5' transform='rotate(-30 -5.98 65)'/%3E%3C/svg%3E");
        }
    }
    */
</style>

<template>
    <div class="container">
        <header-top :title="'云仓'">
            <section slot="left">
                <router-link tag="img" to="/mallOrder" id="go-order-img" src="/static/images/myOrder.png"
                             alt=""></router-link>
            </section>
            <section slot="right">
                <button class="header-btn" @click="gotoShopCart">购物车</button>
            </section>
        </header-top>

        <section class="search-bar-wrap">
            <section class="search-bar">
                <img src="/static/images/search.png" class="icon" alt="">
                <input ref="inputPdNameSearch" type="text" placeholder="搜索商品" v-model.trim="pdNameSearch" @keyup.enter="doSearch">
                <transition name="router-fade">
                    <img v-if="pdNameSearch" src="/static/images/close.png" class="icon"
                         @click="doReset" alt="">
                </transition>
            </section>
        </section>

        <section class="banner">
            <img v-if="banner.mallUrls && banner.mallUrls.length" :src="banner.mallUrls[0].SMurl" alt="">
        </section>

        <!--<div style="width: 100px;height: 60px;border: 1px solid black;"  @dblclick.stop="$toast('双击测试')">双击测试</div>-->
        <!--<button style="width: 100px;height: 60px;border: 1px solid black;" @touch="$toast('触摸测试')">触摸测试</button>-->

        <!-- 一二级分类wrap -->
        <section class="nav-wrap">
            <ul :class="{'nav-list-parent': true, 'none': true}">
                <li v-for="item in parentCategory" :class="{'nav-item': true, 'active': item.PAid == paSelected}"
                    @click="switchPACategory(item)">
                    {{item.PAname}}
                </li>
            </ul>

            <ul class="nav-list-children">
                <li v-for="item in secondCategory" :class="{'pillow-item': true, 'active': item.PAid == secondSelected}"
                    @click="chooseSECategory(item)">
                    {{item.PAname}}
                </li>
            </ul>
        </section>

        <template v-if="productList.length">
            <ul class="goods-list">
                <li class="goods-item" v-for="item in productList" @click="gotoGoodsDetail(item)">
                    <section class="goods-img">
                        <img v-lazy="item.PRpic" alt="">
                    </section>
                    <section class="goods-description">
                        <header class="goods-description-header">
                            <span class="name">{{item.PRname}}</span>
                            <!--<span v-if="item.PRstock < 1000000" class="stock">-->
                            <!--库存: {{item.PRstock}} 件-->
                            <!--</span>-->
                        </header>
                        <section class="goods-description-content">
                            <p class="goods-description-price">
                                <span class="current-price">￥{{item.PRprice}}</span>
                                <span class="original-price">￥{{item.PRoldprice}}</span>
                            </p>

                            <button class="addToCartBtn">加入购物车</button>
                        </section>
                    </section>
                </li>
            </ul>

            <load-more :type="loadingType"></load-more>
        </template>
        <place-holder v-else @click.native="doReset" :title="placeHolderTitle"></place-holder>


        <img src="/static/images/shopcart.png" class="pay-order-fixed" @click="gotoShopCart"/>

        <footer-guide></footer-guide>
    </div>
</template>

<script>
    import footerGuide from "src/components/footer/footerGuide"
    import buyCart from "src/components/common/buyCart"
    import {getProductCategory, getProductList, checkBail} from "src/api/api"
    import LoadMore from "src/components/common/loadMore"
    import common from "src/common/js/common"
    import {mapMutations, mapState, mapGetters} from "vuex"
    import PlaceHolder from "src/components/common/placeHolder"


    export default {
        name: "mall",

        data() {
            return {
                pdNameSearch: '',

                parentCategory: [], //  父级类别
                paSelected: '',    // 父级类别选中的PAid

                secondCategory: [], //  二级类别
                secondSelected: '',    // 二级类别选中的PAid

                productList: [],    //  商品列表
                page: 1,
                count: 10,
                loadingType: 'normal',  // 加载组件加载状态


            }
        },

        components: {
            buyCart,
            footerGuide,
            LoadMore,
            PlaceHolder
        },

        computed: {
            ...mapState(['userInfo', 'banner']),
            placeHolderTitle() {
                if (!this.parentCategory.length) {
                    return '商城还没有一级分类'
                }
                if (!this.secondCategory.length) {
                    return '该类暂时没有没有二级分类'
                }
                if (!this.productList.length) {
                    if(this.pdNameSearch){
                        return '没有符合查询条件的,点击清除'
                    }else{
                        return '该类暂时没有上架的商品'
                    }
                }

            },

        },

        methods: {
            gotoShopCart() {
                this.$router.push('/shopCart');
            },

            doSearch() {
                this.setProductList(true);
                this.$refs.inputPdNameSearch.blur();
            },
            doReset(){
                this.pdNameSearch = '';
                this.setProductList(true);
            },

            gotoGoodsDetail(goods) {
                this.$router.push({
                    path: '/goodsDetail',
                    query: {
                        prid: goods.PRid
                    }
                });
            },

            // 滚动条监听事件
            touchMove() {
                let scrollTop = common.getScrollTop();
                let scrollHeight = common.getScrollHeight();
                let ClientHeight = common.getClientHeight();

                if (scrollTop + ClientHeight >= scrollHeight - 10 && this.loadingType == 'normal') {
                    this.setProductList();
                }
            },


            switchPACategory(categroy) {
                // 选中还是当前父级tab就结束
                if (categroy.PAid == this.paSelected) {
                    return;
                }

                this.paSelected = categroy.PAid;
                this.initSECategory();
            },

            chooseSECategory(categroy) {
                if (categroy.PAid == this.secondSelected) {

                } else {
                    this.secondSelected = categroy.PAid;
                    this.setProductList(true);
                }
            },

            // 初始分类及第一个父级分类的所有商品
            async initCategoryAndPrds() {
                let {data: paData} = await getProductCategory(1, 0);

                paData.unshift({
                    PAname: '全部',
                    PAtype: 1,
                    PAid: 0
                })
                this.parentCategory = paData;
                this.paSelected = this.parentCategory[0].PAid;

                await this.initSECategory();
            },

            async initSECategory() {
                let seData = [];

                if (this.paSelected == 0) {
                    seData = [
                        {
                            PAname: '全部',
                            PAtype: 2,
                            PAid: 0
                        }
                    ]
                } else {
                    let {data} = await getProductCategory(2, this.paSelected);

                    seData = data;
                }

                this.secondCategory = seData;

                if (this.secondCategory[0]) {
                    this.secondSelected = this.secondCategory[0].PAid;

                    await this.setProductList(true);
                } else {
                    this.productList = [];
                }
            },

            /**
             * 获取商品列表
             * @param replace
             */
            async setProductList(replace) {
                if (replace) {
                    this.page = 1;
                }
                this.loadingType = 'loading';

                let {data: prdList} = await getProductList(this.secondSelected ? 2 : 1, this.secondSelected, 1,
                    this.page, this.count,this.pdNameSearch);

                if (prdList.length < this.count) {
                    this.loadingType = 'nomore';
                } else {
                    this.loadingType = 'normal';
                }

                if (replace) {
                    this.productList = prdList;
                } else {
                    this.productList = [...this.productList, ...prdList];
                }

                this.page++;
            },
        },

        destroyed() {
            window.removeEventListener('scroll', this.touchMove);
        },

        async mounted() {
            this.$store.dispatch('getSowingMap');
            await this.initCategoryAndPrds();
            window.addEventListener('scroll', this.touchMove);

            // if(this.$route.query.goOrderList){
            //     this.$router.push('/mallOrder');
            // }
        }
    }
</script>

