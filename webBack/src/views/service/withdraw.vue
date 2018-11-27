<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
    }
</style>

<template>
    <div class="container">
        <!--查询-->
        <section class="tool-tip-wrap">
            <el-form :inline="true" size="small" :model="form">
                <el-form-item label="状态">
                    <el-select v-model="form.status" @change="doSearch">
                        <el-option v-for="option in statusOptions" :label="option.label" :value="option.value"
                                   :key="option.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="doSearch">查询</el-button>
                </el-form-item>
            </el-form>
        </section>

        <!--商品表格-->
        <el-table :data="tableData" v-loading="loading" size="medium" stripe style="width: 100%">
            <el-table-column prop="DMaccountname" align="center" label="户名" width="120"></el-table-column>
            <el-table-column prop="DMamount" align="center" label="金额" width="120"></el-table-column>
            <el-table-column prop="DMbankname" align="center" label="银行名" width="120"></el-table-column>
            <el-table-column prop="DMbranchname" align="center" label="支行" width="120"></el-table-column>
            <el-table-column prop="DMcardnum" align="center" label="卡号" width="220"></el-table-column>
            <el-table-column prop="DMcreatetime" align="center" label="申请时间" width="180"></el-table-column>
            <el-table-column prop="DMstatus" align="center" label="状态" width="120">
                <template slot-scope="scope">
                    {{statusToTxt(scope.row.DMstatus)}}
                </template>
            </el-table-column>
            <el-table-column prop="DMreason" align="center" label="不通过原因" width="180"></el-table-column>
            <el-table-column label="操作" width="220" fixed="right">
                <template slot-scope="scope">
                    <template v-if="scope.row.DMstatus == 1">
                        <el-button type="text" size="small" @click="pass(scope.row)">审核通过</el-button>
                        <el-button type="text" size="small" class="danger-text" @click="noPass(scope.row)">审核不通过
                        </el-button>
                    </template>
                    <template v-if="scope.row.DMstatus == 2">
                        <el-button type="text" size="small" @click="confirmPay(scope.row)">确认打款</el-button>
                    </template>

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
                        label: '待审核',
                    }, {
                        value: 2,
                        label: '待打款',
                    }, {
                        value: 3,
                        label: '已打款',
                    }, {
                        value: 4,
                        label: '未通过',
                    },
                ],
                form: {
                    status: 1
                },

                loading: false,
                total: 0,
                currentPage: 1,
                pageSize: 10,
                tableData: [],

                dialogFormVisible: false,

            }
        },

        components: {},

        computed: {},

        methods: {
            renderHeader(h) {
                return h('el-button', {
                    props: {
                        type: 'primary',
                        // size: 'small'
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

            doSearch(){
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

            setData() {
                this.loading = true;

                this.$http.post(this.$api.getAlluserDrawmoneyList,
                    {
                        status: this.form.status,

                        "page_size": this.pageSize,
                        "page_num": this.currentPage,
                    }, {
                        noLoading: true,
                        params: {
                            token: this.$common.getStore('token')

                        }
                    }).then(
                    res => {
                        this.loading = false;

                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.total = resData.mount|| 0;
                            this.tableData = data;
                        }
                    }
                )
            },

            statusToTxt(status){
                return this.statusOptions.find(item => item.value == status).label;
            },

            async dealWidthDraw(dmid, willstatus, reason = '') {
                let res = await this.$http.post(this.$api.dealDrawmoney, {
                    dmid,
                    willstatus,
                    reason,
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
                let confirm = await  this.$confirm(`确定通过该审核(户名:${row.DMaccountname})?`, '提示', {
                    type: 'info'
                });

                if (confirm) {
                    let result = await this.dealWidthDraw(row.DMid, 2);

                    this.setData()
                    if(result){
                        this.$notify({
                            title: '提现审核已通过',
                            message: `户名:${row.DMaccountname}`,
                            type: 'success'
                        });
                    }
                }


            },
            async noPass(row) {
                let prompt = await this.$prompt('输入不通过原因', '提示', {
                    inputValidator: value => {
                        if(!value){
                            return '原因不能为空!'
                        }
                    }
                });

                if (prompt.value) {
                    let result = await this.dealWidthDraw(row.DMid, 4, prompt.value);

                    this.setData()
                    if(result){
                        this.$notify({
                            title: '提现审核已拒绝',
                            message: `户名:${row.DMaccountname}`,
                            type: 'success'
                        });
                    }
                }else{

                }
            },
            async confirmPay(row) {
                let confirm = await  this.$confirm(`确定已经打款(户名:${row.DMaccountname})?`, '提示', {
                    type: 'info'
                });

                if (confirm) {
                    let result = await this.dealWidthDraw(row.DMid, 3);

                    this.setData()
                    if(result){
                        this.$notify({
                            title: '提现已打款',
                            message: `户名:${row.DMaccountname}`,
                            type: 'success'
                        });
                    }
                }
            },



            handleRemove(file, fileList) {
                console.log(file, fileList);
            },
            handlePictureCardPreview(file) {
                this.dialogImageUrl = file.url;
                this.dialogVisible = true;
            }
        },

        created() {
            this.setData();
        },
    }
</script>

