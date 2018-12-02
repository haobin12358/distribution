<template>
    <div class="container">
        <header-top :show-back="true"></header-top>
        <section class="search-bar-wrap">
            <section class="search-bar">
                <img src="/static/images/search.png" class="icon" alt="">
                <input type="text" placeholder="搜索商品" v-model.trim="pdNameSearch" @keyup.enter="doSearch">
                <transition name="router-fade">
                    <img v-if="pdNameSearch" src="/static/images/close.png" class="icon"
                         @click="pdNameSearch = ''" alt="">
                </transition>
            </section>
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
        <place-holder v-else title="换个商品名试试"></place-holder>
    </div>
</template>

<script>
    import PlaceHolder from "src/components/common/placeHolder"
    import LoadMore from "src/components/common/loadMore"
    import { getProductList} from "src/api/api"
    import common from "src/common/js/common"


    export default {
        name: "productSearch",

        components: {
            PlaceHolder,
            LoadMore
        },

        data() {
            return {
                pdNameSearch: '',

                productList: [],    //  商品列表
                page: 1,
                count: 10,
                loadingType: 'normal',  // 加载组件加载状态
            }
        },

        computed: {},

        methods: {
            doSearch(){
                this.setProductList(true);
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
                let {data: prdList, mount} = await getProductList(1, 0, 1, this.page, this.count,this.pdNameSearch);

                if (prdList.length < this.count) {
                    this.loadingType = 'nomore';
                } else {
                    this.loadingType = 'normal';
                }

                if (replace) {
                    this.productList = prdList;
                    this.$toast(`共搜索出${mount}件商品`)
                } else {
                    this.productList = [...this.productList, ...prdList];
                }

                this.page++;
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

            gotoGoodsDetail(goods) {
                this.$router.push({
                    path: '/goodsDetail',
                    query: {
                        prid: goods.PRid
                    }
                });
            },
        },

        destroyed(){
            window.removeEventListener('scroll', this.touchMove);

        },

        mounted() {
            this.setProductList(true);
            window.addEventListener('scroll', this.touchMove);
        },
    }
</script>

<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .least-full-screen();

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
    }


</style>
