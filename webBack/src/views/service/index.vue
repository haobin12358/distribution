<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
    }
</style>

<template>
    <div class="container">
        <section class="tool-tip-wrap">
            <el-form :inline="true" size="small" :model="formInline" class="demo-form-inline">
                <el-form-item label="状态">
                    <el-select v-model="formInline.status" @change="doSearch">
                        <el-option v-for="option in statusOptions" :label="option.label" :value="option.value"
                                   :key="option.value">
                        </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" icon="el-icon-search" @click="doSearch">查询</el-button>
                </el-form-item>
            </el-form>
        </section>

        <!--商品表格-->
        <el-table :data="tableData" v-loading="loading" stripe style="width: 100%">
            <el-table-column prop="USname" align="center" label="用户名" width="180"></el-table-column>
            <el-table-column prop="USphonenum" align="center" label="手机号" width="180"></el-table-column>
            <el-table-column prop="CMcontent" align="center" label="反馈内容" ></el-table-column>
            <el-table-column prop="CMcontent" align="center" label="状态" width="120">
                <template slot-scope="scope">
                    {{statusToTxt(scope.row.CMstatus)}}
                </template>
            </el-table-column>
            <el-table-column prop="CMcreatetime" align="center" label="日期" width="180"></el-table-column>
            <el-table-column label="操作" width="120" fixed="right">
                <template slot-scope="scope">
                    <el-button type="text" size="small" @click="dealComment(scope.row)">处理</el-button>
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
                statusOptions: [
                    {
                        value: 0,
                        label: '全部',
                    }, {
                        value: 1,
                        label: '待处理',
                    }, {
                        value: 2,
                        label: '已处理',
                    },
                ],
                formInline: {
                    status: 1
                },


                loading: false,
                total: 0,
                currentPage: 1,
                pageSize: 10,
                tableData: [],


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
                            this.doSim();
                        }
                    }
                }, '新增')

            },
            doSim() {
                this.dialogFormVisible = true;
            },


            doSearch() {
                this.currentPage = 1;
                this.setData();
            },

            sizeChange(pageSize) {
                this.pageSize = pageSize;
                this.currentPage = 1;

                this.setData();
            },
            pageChange(page) {
                this.currentPage = page;
                this.setData();
            },

            statusToTxt(status){
                return this.statusOptions.find(item => item.value == status).label;
            },

            setData() {
                this.loading = true;
                this.$http.get(this.$api.getCommentList
                    , {
                        noLoading: true,
                        params: {
                            token: this.$common.getStore('token'),

                            "status": this.formInline.status,
                            "page_size": this.pageSize,
                            "page_num": this.currentPage,
                        }
                    }).then(
                    res => {
                        this.loading = false;

                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.total = resData.mount || 0;
                            this.tableData = data;
                        }
                    }
                )
            },

            dealComment(item){
                this.$confirm(`确定已处理(用户名:${item.USname})的反馈?`, '提示', {
                    type: 'warning'
                }).then(
                    () => {
                        this.$http.post(this.$api.dealComments,{
                            cmid: item.CMid
                        },{
                            params: {
                                token: this.$common.getStore('token')

                            }
                        }).then(
                            res => {
                                if (res.data.status == 200) {
                                    let resData = res.data,
                                        data = res.data.data;

                                    this.setData();
                                    this.$notify({
                                        title: '反馈处理成功',
                                        message: `用户名:${item.USname}`,
                                        type: 'success'
                                    });
                                }
                            }
                        )
                    }
                )

            }
        },

        created() {
            this.setData();
        },
    }
</script>

