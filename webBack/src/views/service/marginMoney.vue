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
            <el-table-column prop="USname" align="center" label="用户名" width="120"></el-table-column>
            <el-table-column prop="USphonenum" align="center" label="手机号" width="120"></el-table-column>
            <el-table-column prop="BRtradenum" align="center" label="流水号"></el-table-column>
            <el-table-column prop="BRmount" align="center" label="金额" width="180"></el-table-column>
            <el-table-column prop="BRstatus" align="center" label="状态" width="120">
                <template slot-scope="scope">
                    {{statusToTxt(scope.row.BRstatus)}}
                </template>
            </el-table-column>
            <el-table-column prop="BRcreatetime" align="center" label="申请时间" width="180"></el-table-column>
            <el-table-column label="操作" width="220" fixed="right">
                <template slot-scope="scope">
                    <el-button v-if="scope.row.BRstatus == 2" type="text" size="small" @click="pass(scope.row)">审核通过</el-button>
                    <el-button v-if="scope.row.BRstatus == 2" type="text" class="danger-text" size="small" @click="noPass(scope.row)">审核不通过</el-button>
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
        name: "marginMoney",

        data() {
            return {
                statusOptions: [
                    {
                        value: 0,
                        label: '全部',
                    }, {
                        value: 1,
                        label: '已充值',
                    }, {
                        value: 2,
                        label: '退还中',
                    }, {
                        value: 3,
                        label: '已退还',
                    }, {
                        value: 4,
                        label: '退还失败',
                    },
                ],
                formInline: {
                    status: 2
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

            statusToTxt(status) {
                return this.statusOptions.find(item => item.value == status).label;
            },

            setData() {
                this.loading = true;
                this.$http.post(this.$api.getAllUserBailRecord, {
                        "status": this.formInline.status,
                        "page_size": this.pageSize,
                        "page_num": this.currentPage,
                    }
                    , {
                        noLoading: true,
                        params: {
                            token: this.$common.getStore('token'),
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

            async dealBailRecord(brid, willstatus) {
                let res = await this.$http.post(this.$api.dealBailRecord, {
                    brid,
                    willstatus
                }, {
                    params: {
                        token: this.$common.getStore('token')
                    }
                });

                if (res.data.status == 200) {
                    return true;
                } else {
                    return false;
                }
            },

            async pass(row) {
                let confirm = await  this.$confirm(`确定通过该审核(流水号:${row.BRtradenum})?`, '提示', {
                    type: 'info'
                });

                if (confirm) {
                    let result = await this.dealBailRecord(row.BRid, 3);

                    this.setData()
                    if(result){
                        this.$notify({
                            title: '保证金已退还',
                            message: `流水号:${row.BRtradenum}`,
                            type: 'success'
                        });
                    }
                }


            },
            async noPass(row) {
                let confirm = await  this.$confirm(`确定不通过该审核(流水号:${row.BRtradenum})?`, '提示', {
                    type: 'warning'
                });

                if (confirm) {
                    let result = await this.dealBailRecord(row.BRid, 4);

                    this.setData()
                    if(result){
                        this.$notify({
                            title: '保证金退还审核已拒绝',
                            message: `流水号:${row.BRtradenum}`,
                            type: 'success'
                        });
                    }
                }
            },
        },

        created() {
            this.setData();
        },
    }
</script>

