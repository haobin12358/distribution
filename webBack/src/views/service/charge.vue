<style lang="less" scoped>
    @import "../../common/css/index";

    .container {

        .demo-table-expand {
            font-size: 0;
        }
        .demo-table-expand label {
            width: 90px;
            color: #99a9bf;
        }
        .demo-table-expand .el-form-item {
            margin-right: 0;
            margin-bottom: 0;
            width: 50%;
        }

        .small-proof-img {
            .wl(1rem, 1rem);
            border: 1px solid black;
            margin-right: .3rem;
        }
        .proof-img {
            max-width: 100%;
            max-height: 100%;
        }
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
        <el-table :data="tableData" v-loading="loading" size="medium" :cell-class-name="cellFunction" stripe
                  style="width: 100%">
            <el-table-column prop="username" align="center" width="120" label="用户名"></el-table-column>
            <el-table-column prop="userphonenum" align="center" width="120" label="手机号"></el-table-column>
            <el-table-column prop="CMamount" align="center" label="金额" width="120"></el-table-column>
            <el-table-column prop="type" align="center" label="用户打款方式" width="120">
                <template slot-scope="scope">
                    {{scope.row.CMalipaynum ? '支付宝' : '银行转账'}}
                </template>
            </el-table-column>
            <el-table-column prop="info" align="center" label="账号信息" width="200">
                <template slot-scope="scope">
                    {{scope.row.CMalipaynum ? scope.row.CMalipaynum : `${scope.row.CMbankname}
                    ${scope.row.CMaccountname} ${scope.row.CMcardnum}`}}
                </template>
            </el-table-column>
            <el-table-column prop="CMpaytime" align="center" label="充值日期" width="120"></el-table-column>
            <el-table-column prop="name" align="center" label="凭证" width="200">
                <template slot-scope="scope">
                    <img v-for="item in scope.row.CMproof" class="small-proof-img" v-lazy="item"
                         @click="showBigImg(item)" alt="">
                </template>
            </el-table-column>
            <el-table-column prop="CMcreatetime" align="center" label="申请日期" width="180"></el-table-column>
            <el-table-column prop="CMstatus" align="center" label="状态" width="120">
                <template slot-scope="scope">
                    {{statusToTxt(scope.row.CMstatus)}}
                </template>
            </el-table-column>
            <el-table-column prop="CMreason" align="center" label="不通过原因" width="180"></el-table-column>
            <el-table-column prop="CMremark" align="center" label="备注" width="120"></el-table-column>

            <el-table-column label="操作" width="220" fixed="right">
                <template slot-scope="scope">
                    <template v-if="scope.row.CMstatus == 1">
                        <el-button type="text" size="small" @click="pass(scope.row)">审核通过</el-button>
                        <el-button type="text" class="danger-text" size="small" @click="noPass(scope.row)">审核不通过
                        </el-button>
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

        <el-dialog title="打款凭证" :visible.sync="dialogTableVisible">
            <img class="proof-img" v-lazy="bigImgUrl" alt="">
        </el-dialog>
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
                        label: '已充值',
                    }, {
                        value: 3,
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

                bigImgUrl: '',
                dialogTableVisible: false,

            }
        },

        components: {},

        computed: {},

        methods: {
            showBigImg(url) {
                this.bigImgUrl = url;
                this.dialogTableVisible = true;
            },

            doSearch() {
                this.currentPage = 1;
                this.setData();
            },


            cellFunction({row, column}) {
                if (column.property == 'CMamount') {
                    return 'money-cell'
                }
                else if (column.property == 'info') {
                    return 'primary-cell'

                }

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

                this.$http.post(this.$api.getAllChargemoney,
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

                            this.total = resData.mount || 0;
                            this.tableData = data;
                        }
                    }
                )
            },

            statusToTxt(status) {
                return this.statusOptions.find(item => item.value == status).label;
            },

            async dealWidthDraw(cmid, willstatus, reason = '') {
                let res = await this.$http.post(this.$api.dealChargemoney, {
                    cmid,
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
                let confirm = await this.$confirm(`确定通过该审核(用户名:${row.CMaccountname})?`, '提示', {
                    type: 'info'
                });

                if (confirm) {
                    let result = await this.dealWidthDraw(row.CMid, 2);

                    this.setData()
                    if (result) {
                        this.$notify({
                            title: '充值审核已通过',
                            message: `用户名:${row.CMaccountname}余额冲入${row.CMamount}元`,
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
                    let result = await this.dealWidthDraw(row.CMid, 3, prompt.value);

                    this.setData();
                    if (result) {
                        this.$notify({
                            title: '充值审核已拒绝',
                            message: `用户名:${row.CMaccountname}`,
                            type: 'success'
                        });
                    }
                } else {
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

