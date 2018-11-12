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
                    <el-input v-model.trim="formInline.PRname" :clearable="true" placeholder="商品名"></el-input>
                </el-form-item>

                <el-form-item label="分类">
                    <el-cascader
                        :options="options"
                        :props="cascaderProps"
                        :clearable="true"
                        v-model="formInline.CAselect"
                    @change="setProductList">
                    </el-cascader>
                </el-form-item>
                <el-form-item label="状态">
                    <el-select v-model="formInline.PRstatus" @change="setProductList">
                        <el-option v-for="option in statusOptions" :label="option.label" :value="option.value"
                                   :key="option.value">
                        </el-option>
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
                    <img v-lazy="scope.row.PRpic" class="table-pic"/>
                </template>
            </el-table-column>
            <el-table-column prop="PRname" label="商品名" width="180" align="center"></el-table-column>
            <el-table-column label="所属分类" width="180" align="center">
                <template slot-scope="scope">
                    {{`${scope.row.firstpaname} /${scope.row.categoryname}`}}
                </template>
            </el-table-column>
            <el-table-column prop="PRoldprice" label="原价格" align="center"></el-table-column>
            <el-table-column prop="PRprice" label="折后价格" align="center"></el-table-column>
            <el-table-column prop="PRstatus" label="状态" align="center">
                <template slot-scope="scope">
                    {{statusToTxt(scope.row.PRstatus)}}
                </template>
            </el-table-column>
            <el-table-column prop="PRlogisticsfee" label="邮费" align="center"></el-table-column>
            <el-table-column prop="PAdiscountnum" label="返点件数" align="center"></el-table-column>
            <el-table-column prop="PRstock" label="库存" align="center"></el-table-column>
            <el-table-column prop="PRcreatetime" label="创建时间" width="180" align="center"></el-table-column>

            <el-table-column label="操作" width="120" fixed="right" align="left" :render-header="renderHeader">
                <template slot-scope="scope">
                    <el-button type="text" size="small" @click="handleEdit(scope.row)">编辑</el-button>
                    <el-button v-if="scope.row.PRstatus == 1" @click="handleDelete(scope.row)" style="color: red;" type="text" size="small">下架</el-button>
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
                statusOptions:[
                    {
                        value: 0,
                        label: '全部',
                    },{
                        value: 1,
                        label: '出售中',
                    },{
                        value: 2,
                        label: '已售罄',
                    },{
                        value: 3,
                        label: '已下架',
                    },
                ],
                //  查询表单
                formInline: {
                    PRname: '',
                    CAselect: [],
                    PRstatus: 1,
                },
                //  商品分类选项
                options: [

                ],
                cascaderProps: {
                    value: 'PAid',
                    label: 'PAname',
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
                return h('el-button', {
                    props: {
                        type: 'primary',
                    },
                    on: {
                        click: () => {
                            this.doAddPd();
                        }
                    }
                }, '新增');
            },

            doAddPd(){
                this.$router.push('/productEdit');
            },

            handleEdit(pd) {
                this.$router.push({
                    path: 'productEdit',
                    query: {
                        pd
                    }
                })
            },
            handleDelete(pd) {
                this.$confirm(`确定要下架商品:${pd.PRname}?`, '提示',{
                    type: 'warning'
                }).then(
                    () => {
                        this.$http.post(this.$api.withdrawProduct,{
                            prid: pd.PRid,
                        },{
                            params: {
                                token: this.$common.getStore('token')
                            }
                        }).then(
                            res => {
                                if (res.data.status == 200) {
                                    let resData = res.data,
                                        data = res.data.data;

                                    this.setProductList();
                                    this.$notify({
                                        title: '商品下架成功',
                                        message: `商品名:${pd.PRname}`,
                                        type: 'success'
                                    });
                                }
                            }
                        )
                    }
                )
            },

            setCategoryList() {
                this.$http.get(this.$api.getProductCategoryList,{
                    noLoading: true
                }).then(
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
                this.currentPage = 1;
                this.setProductList();
            },

            doReset() {
                this.currentPage = 1;

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
                    noLoading: true,

                    params: {
                        page_size: this.pageSize,
                        page_num: this.currentPage,
                        PRstatus: this.formInline.PRstatus,
                        PAid: this.formInline.CAselect.length?this.formInline.CAselect[1]: 0,
                        PAtype:this.formInline.CAselect.length?'2': '1',
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
            },

            statusToTxt(status){
                return this.statusOptions.find(item => item.value == status).label;
            }

        },

        created() {
            this.currentPage = 1;
            this.setCategoryList();
            this.setProductList();
        },
    }
</script>

