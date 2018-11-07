<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
    }
</style>

<template>
    <div class="container">
        <!--查询-->
        <section class="tool-tip-wrap">
            <el-form :inline="true" size="small" :model="formInline" class="demo-form-inline">
                <el-form-item type="index"></el-form-item>

                <el-form-item label="名称">
                    <el-input v-model.trim="formInline.PRname" placeholder="商品名"></el-input>
                </el-form-item>

                <el-form-item label="分类">
                    <el-cascader
                        :options="options"
                        :props="cascaderProps"
                        v-model="formInline.CAselect">
                    </el-cascader>
                </el-form-item>
                <el-form-item label="状态">
                    <el-select v-model="formInline.PRstatus">
                        <el-option label="全部" value="0"></el-option>
                        <el-option label="出售中" value="1"></el-option>
                        <el-option label="已售罄" value="2"></el-option>
                        <el-option label="已下架" value="3"></el-option>
                    </el-select>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" icon="el-icon-search" @click="doSearch">查询</el-button>
                    <el-button @click="doReset" icon="el-icon-refresh">重置</el-button>
                </el-form-item>
            </el-form>
        </section>
        <!--商品表格-->
        <el-table :data="tableData" v-loading="loading" stripe style="width: 100%">
            <el-table-column prop="img" align="center" label="图片" width="120">
                <template slot-scope="scope">
                    <img :src="scope.row.PRpic" class="table-pic"/>
                </template>
            </el-table-column>
            <el-table-column prop="PRname" label="商品名" width="180" align="center"></el-table-column>
            <el-table-column prop="categoryname" label="所属分类" width="180" align="center"></el-table-column>
            <el-table-column prop="PRoldprice" label="原价格" align="center"></el-table-column>
            <el-table-column prop="PRprice" label="折后价格" align="center"></el-table-column>
            <el-table-column prop="PRlogisticsfee" label="邮费" align="center"></el-table-column>
            <el-table-column prop="PAdiscountnum" label="返点件数" align="center"></el-table-column>
            <el-table-column prop="PRstock" label="库存" align="center"></el-table-column>
            <el-table-column prop="PRcreatetime" label="创建时间" width="180" align="center"></el-table-column>

            <el-table-column label="操作" width="120" fixed="right" align="center" :render-header="renderHeader">
                <template slot-scope="scope">
                    <el-button type="text" size="small">编辑</el-button>
                </template>
            </el-table-column>
        </el-table>


        <section style="display: flex; justify-content: center">
            <el-pagination
                style="margin-top: .5rem"
                :current-page="currentPage"
                :page-sizes="[10, 20, 30, 40]"
                :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="total"
                @size-change="sizeChange"
                @current-change="pageChange">
            </el-pagination>
        </section>
    </div>
</template>

<script>


    export default {
        name: "index",

        data() {
            return {
                //  查询表单
                formInline: {
                    PRname: '',
                    CAselect: [],
                    PRstatus: '0',
                },
                //  商品分类选项
                options: [

                ],
                cascaderProps: {
                    value: 'PAid',
                    label: 'Parentname',
                    children: 'child_category',
                },


                loading: false,
                total: 0,
                currentPage: 1,
                pageSize: 10,
                tableData: [],
                search: '',


            }
        },

        components: {},

        computed: {},

        methods: {
            renderHeader(h) {
                return (
                    <router-link tag="el-button" to="productEdit" type="primary">
                        新增
                    </router-link>

                )
            },
            handleEdit() {
            },
            handleDelete() {
            },

            setCategoryList() {
                this.$http.get(this.$api.getProductCategoryList).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.options = data;
                        }
                    }
                )
            },

            doSearch() {
                this.setProductList();
            },

            doReset() {
                this.formInline.PRname = '';
                this.formInline.CAselect = [];
                this.formInline.PRstatus = '0';

                this.setProductList();
            },


            sizeChange(pageSize) {
                this.pageSize = pageSize;
                this.currentPage = 1;

                this.setProductList();
            },
            pageChange(page) {
                this.currentPage = page;
                this.setProductList();
            },
            setProductList() {
                this.loading = true;
                this.$http.get(this.$api.getProductList, {
                    params: {
                        page_size: this.pageSize,
                        page_num: this.currentPage,
                        PRstatus: this.formInline.PRstatus,
                        PAid: 0,
                        PAtype: '1',
                        PRname: this.formInline.PRname
                    }
                }).then(
                    res => {
                        if (res.data.status == 200) {
                            this.loading = false;
                            this.tableData = res.data.data;
                            this.total = res.data.mount;
                        }
                    }
                )
            }

        },

        created() {
            this.currentPage = 1;
            this.setCategoryList();
            this.setProductList();
        },
    }
</script>

