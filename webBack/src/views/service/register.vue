<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .proof-img {
            max-width: 100%;
            max-height: 100%;
        }

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

                <el-form-item>

                <el-switch
                    v-model="expandAll"
                    active-text="展开"
                    inactive-text="不展开"
                    active-color="#13ce66"
                    inactive-color="#ff4949"
                    @change="changeSwitch">
                </el-switch>
                </el-form-item>
            </el-form>
        </section>
        <!--商品表格-->
        <el-table ref="regTable" :data="tableData" v-loading="loading" size="mini" @row-click="expandRow" stripe
                  :default-expand-all="expandAll" style="width: 100%">
            <el-table-column type="expand">
                <template slot-scope="props">
                    <el-form label-position="left" inline class="demo-table-expand">
                        <el-form-item label="推荐人姓名">
                            <span>{{ props.row.IRIprename }}</span>
                        </el-form-item>
                        <el-form-item label="推荐人手机号">
                            <span>{{ props.row.IRIprephonenum }}</span>
                        </el-form-item>
                        <el-form-item label="姓名">
                            <span>{{ props.row.IRIname }}</span>
                        </el-form-item>
                        <el-form-item label="手机号">
                            <span>{{ props.row.IRIphonenum }}</span>
                        </el-form-item>
                        <el-form-item label="微信号">
                            <span>{{ props.row.IRIwechat }}</span>
                        </el-form-item>
                        <el-form-item label="地址">
                            <span>{{ props.row.address }} {{ props.row.IRIaddress }}</span>
                        </el-form-item>
                        <el-form-item label="打款时间">
                            <span>{{ props.row.IRIpaytime }}</span>
                        </el-form-item>
                        <el-form-item label="注册金">
                            <span>{{ props.row.IRIpayamount }}</span>
                        </el-form-item>
                        <el-form-item label="打款方式">
                            <span>{{ props.row.IRIpaytype == 1 ? '支付宝' : '银行转账'}}</span>
                        </el-form-item>
                        <el-form-item label="打款信息">
                            <span>{{ props.row.IRIpaytype == 1
                                ? props.row.IRIalipaynum
                                : `${props.row.IRIbankname} ${props.row.IRIaccountname} ${props.row.IRIcardnum}`}}</span>
                        </el-form-item>

                    </el-form>
                </template>
            </el-table-column>

            <el-table-column prop="IRIprename" align="center" label="推荐人姓名" width="120"></el-table-column>
            <el-table-column prop="IRIname" align="center" label="姓名" ></el-table-column>
            <el-table-column prop="IRIphonenum" align="center" label="手机号" width="120"></el-table-column>
            <el-table-column prop="IRIwechat" align="center" label="微信" width="120"></el-table-column>
            <el-table-column prop="IRIpayamount" align="center" label="注册金" width="120"></el-table-column>
            <el-table-column align="center" label="状态" width="120">
                <template slot-scope="scope">
                    {{statusToTxt(scope.row.IRIstatus)}}
                </template>
            </el-table-column>
            <el-table-column prop="name" align="center" label="凭证" width="200">
                <template slot-scope="scope">
                    <img v-for="item in scope.row.IRIproof" class="table-pic" style="margin-right: .2rem;" v-lazy="item"  @click="showBigImg(item)" alt="">
                </template>
            </el-table-column>
            <el-table-column label="操作" width="180" align="center" fixed="right">
                <template slot-scope="scope">
                    <template v-if="scope.row.IRIstatus == 1">
                        <el-button type="text" size="small" @click.stop="pass(scope.row)">审核通过</el-button>
                        <el-button type="text" class="danger-text" size="small" @click.stop="noPass(scope.row)">审核不通过</el-button>

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

            <img class="proof-img" :src="bigImgUrl" alt="">

        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "index",

        data() {
            return {
                expandAll: true,

                statusOptions: [
                    {
                        value: 0,
                        label: '全部',
                    }, {
                        value: 1,
                        label: '未审核',
                    }, {
                        value: 2,
                        label: '已通过',
                    },{
                        value: 3,
                        label: '未通过',
                    },
                ],
                formInline: {
                    status: 1,
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
            changeSwitch() {
                for (let i = 0; i < this.tableData.length; i++) {
                    this.$refs.regTable.toggleRowExpansion(this.tableData[i], this.expandAll);
                }
            },

            showBigImg(url){
                this.bigImgUrl = url;
                this.dialogTableVisible = true;
            },


            expandRow(row) {
                this.$refs.regTable.toggleRowExpansion(row);
            },

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

            setData(){
                this.loading = true;
                this.expandAll = true;
                this.$http.post(this.$api.getRegisterRecord,{
                    "status": this.formInline.status,

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

                            this.total = resData.mount;
                            this.tableData = data;
                        }
                    }
                )
            },

            async dealWidthDraw(IRIid, willstatus) {
                let res = await this.$http.post(this.$api.dealRegisterRecord, {
                    IRIid,
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
                let confirm = await  this.$confirm(`确定通过该审核(用户名:${row.IRIname})?`, '提示', {
                    type: 'info'
                });

                if (confirm) {
                    let result = await this.dealWidthDraw(row.IRIid, 2);

                    this.setData()
                    if(result){
                        this.$notify({
                            title: '注册审核已通过',
                            message: `用户名:${row.IRIname}`,
                            type: 'success'
                        });
                    }
                }


            },
            async noPass(row) {
                let confirm = await  this.$confirm(`确定不通过该审核(用户名:${row.IRIname})?`, '提示', {
                    type: 'warning'
                });

                if (confirm) {
                    let result = await this.dealWidthDraw(row.IRIid, 3);

                    this.setData()
                    if(result){
                        this.$notify({
                            title: '注册审核已拒绝',
                            message: `用户名:${row.IRIname}`,
                            type: 'success'
                        });
                    }
                }
            },

            statusToTxt(status){
                return this.statusOptions.find(item => item.value == status).label;
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

