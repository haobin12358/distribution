<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
    }
</style>

<template>
    <div class="container">
        <el-breadcrumb style="margin-bottom: .2rem;" separator="/">
            <el-breadcrumb-item>所有订单</el-breadcrumb-item>
        </el-breadcrumb>
        <!--查询栏-->
        <section class="tool-tip-wrap">
            <el-form :inline="true" size="small" :model="formInline" class="demo-form-inline">
                <el-form-item label="订单号">
                    <el-input v-model.trim="formInline.oisn" :clearable="true" placeholder="订单号"></el-input>
                </el-form-item>
                <el-form-item label="下单时间">
                    <el-col :span="11">
                        <el-date-picker type="date" v-model="formInline.starttime" placeholder="起始日期"
                                        style="width: 100%;"></el-date-picker>
                    </el-col>
                    <el-col class="middle-line" :span="2">-</el-col>
                    <el-col :span="11">
                        <el-date-picker type="date" v-model="formInline.endtime" placeholder="结束日期"
                                        style="width: 100%;"></el-date-picker>
                    </el-col>
                </el-form-item>
                <el-form-item label="收件人">
                    <el-input v-model.trim="formInline.username" :clearable="true" placeholder="用户名"></el-input>
                </el-form-item>
                <el-form-item label="手机号">
                    <el-input v-model.trim="formInline.userphonenum" :clearable="true" placeholder="手机号"></el-input>
                </el-form-item>
                <el-form-item label="商品名">
                    <el-input v-model.trim="formInline.productname" :clearable="true" placeholder="商品名"></el-input>
                </el-form-item>

                <el-form-item label="状态">
                    <el-select v-model="formInline.status" @change="setOrderList">
                        <el-option v-for="option in statusOptions" :label="option.label" :value="option.value"
                                   :key="option.value">
                        </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" icon="el-icon-search" @click="doSearch">查询</el-button>
                    <el-button @click="doReset" icon="el-icon-refresh">重置</el-button>
                    <el-button type="info" icon="el-icon-download" @click="exportOrder">导出待发货订单</el-button>

                </el-form-item>

            </el-form>
            <el-switch
                v-model="expandAll"
                active-text="展开"
                inactive-text="不展开"
                active-color="#13ce66"
                inactive-color="#ff4949"
                @change="changeSwitch">
            </el-switch>
        </section>


        <!--订单-->
        <el-table :data="tableData" v-loading="loading" ref="orderTable" size="small" :default-expand-all="expandAll"
                  style="width: 100%" @row-click="expandRow" :cell-class-name="cellFunction" @selection-change="handleSelectionChange">
            <el-table-column
                type="selection"
                width="55">
            </el-table-column>
            <el-table-column type="expand">
                <template slot-scope="props">
                    <el-table :data="props.row.product_list" size="small" stripe :cell-class-name="subCellFunction"
                              style="width: 100%">
                        <el-table-column prop="img" align="center" label="图片" width="180">
                            <template slot-scope="scope">
                                <img v-lazy="scope.row.PRimage" :key="scope.row.PRimage" class="table-pic" alt="">
                            </template>
                        </el-table-column>
                        <el-table-column prop="PRname" align="center" label=" 商品名" width="240"></el-table-column>
                        <el-table-column prop="PRprice" align="center" label="单价" width="120"></el-table-column>
                        <el-table-column prop="colorname" align="center" label="颜色" width="120"></el-table-column>
                        <el-table-column prop="sizename" align="center" label="尺码" width="120"></el-table-column>
                        <el-table-column prop="number" align="center" label="数量" width="120"></el-table-column>
                    </el-table>
                </template>
            </el-table-column>
            <el-table-column prop="OIsn" align="center" label="订单号" width="280"></el-table-column>
            <el-table-column prop="username" align="center" label="收件人" width="180"></el-table-column>
            <el-table-column prop="userphonenum" align="center" label="手机号" width="160"></el-table-column>
            <el-table-column prop="OImount" label="总价" align="center"></el-table-column>
            <el-table-column label="状态" width="120" align="center">
                <template slot-scope="scope">
                    {{statusToTxt(scope.row.OIstatus)}}
                </template>
            </el-table-column>
            <el-table-column prop="OIcreatetime" label="下单时间" align="center" width="180"></el-table-column>

            <el-table-column label="快递信息" width="180" align="center">
                <template slot-scope="scope">
                    {{`${scope.row.expressname || ''} ${scope.row.expressnum || ''}`}}
                </template>
            </el-table-column>

            <!--操作-->
            <el-table-column label="操作" width="120" fixed="right" align="center">
                <template slot-scope="scope">
                    <el-button v-if="scope.row.OIstatus == 2" type="text" size="small"
                               @click.stop="gotoOrderDetail(scope.row)">查看
                    </el-button>
                    <el-button v-if="scope.row.OIstatus == 3" type="text" size="small"
                               @click.stop="gotoOrderDetail(scope.row)">查看
                    </el-button>
                    <el-button v-if="scope.row.OIstatus == 4" type="text" size="small"
                               @click.stop="gotoOrderDetail(scope.row)">去发货
                    </el-button>
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

        <el-dialog title="收货地址" :visible.sync="dialogTableVisible">
            <el-table :data="waitDeliverData">
                <el-table-column property="date" label="日期" width="150"></el-table-column>
                <el-table-column property="name" label="姓名" width="200"></el-table-column>
                <el-table-column property="address" label="地址"></el-table-column>
            </el-table>
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
                        value: 5,
                        label: '已取消',
                    },{
                        value: 1,
                        label: '待发货',
                    }, {
                        value: 4,
                        label: '拣货中',
                    }, {
                        value: 2,
                        label: '已发货',
                    }, {
                        value: 3,
                        label: '已完成',
                    },
                ],
                formInline: {
                    user: '',
                    oisn: "",
                    status: 1,
                    username: "",
                    userphonenum: "",
                    productname: "",
                    starttime: '',
                    endtime: '',
                },

                expandAll: true,
                loading: false,
                total: 0,
                currentPage: 1,
                pageSize: 10,
                tableData: [],

                dialogTableVisible: false,
                waitDeliverData: [],
            }
        },

        components: {},

        computed: {},

        methods: {
            expandRow(row) {
                this.$refs.orderTable.toggleRowExpansion(row);
            },
            gotoOrderDetail(order) {
                this.$router.push({
                    path: 'orderDetail',
                    query: order
                })
            },

            doSearch() {
                this.setOrderList();
            },
            doReset() {
                this.formInline = {
                    user: '',
                    oisn: "",
                    status: 0,
                    username: "",
                    userphonenum: "",
                    productname: "",
                    starttime: '',
                    endtime: '',
                }

                this.setOrderList();
            },
            changeSwitch() {
                for (let i = 0; i < this.tableData.length; i++) {
                    this.$refs.orderTable.toggleRowExpansion(this.tableData[i], this.expandAll);
                }
            },

            cellFunction({row, column}) {
                if (column.property == 'OImount') {
                    return 'money-cell'
                } else {
                    return 'primary-cell'
                }
            },
            subCellFunction({row, column}) {
                // if (column.property == 'PRprice' || column.property == 'PRnum') {
                //     return 'money-cell'
                // } else {
                return 'primary-cell'
                // }
            },

            sizeChange(pageSize) {
                this.pageSize = pageSize;
                this.currentPage = 1;

                this.setOrderList();
            },
            pageChange(page) {
                this.currentPage = page;
                this.setOrderList();
            },

            setOrderList() {
                this.loading = true;
                this.expandAll = true;
                this.$http.post(this.$api.getAllOrder,
                    {
                        "page_size": this.pageSize,
                        "page_num": this.currentPage,
                        "oisn": this.formInline.oisn,
                        "starttime": this.$common.dateFormat(this.formInline.starttime),
                        "endtime": this.$common.dateFormat(this.formInline.endtime),
                        "status": this.formInline.status,
                        "username": this.formInline.username,
                        "userphonenum": this.formInline.userphonenum,
                        "productname": this.formInline.productname,
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

                            data = this.handleSkuList(data);

                            this.tableData = data;
                            this.total = resData.mount || 0;
                        }
                    }
                )
            },
            //  将三层的变成两层
            handleSkuList(data) {
                for (let i = 0; i < data.length; i++) {
                    let newPdlist = [];

                    for (let j = 0; j < data[i].product_list.length; j++) {
                        let cuProd = data[i].product_list[j],
                            newProd = [];

                        for (let k = 0; k < cuProd.skulist.length; k++) {
                            let cuSku = cuProd.skulist[k];

                            newProd.push({
                                PRimage: cuProd.PRimage,
                                PRname: cuProd.PRname,
                                PRprice: cuProd.PRprice,
                                colorname: cuSku.colorname,
                                sizename: cuSku.sizename,
                                number: cuSku.number,
                            })
                        }

                        newPdlist = newPdlist.concat(newProd);
                    }

                    data[i].product_list = newPdlist;
                }

                return data;
            },
            exportOrder() {
                if(this.waitDeliverData.length && this.formInline.status == 1){
                    this.$confirm(`确认导出${this.waitDeliverData.length}个订单?`).then(
                        () => {
                            this.$http.post(this.$api.getWillSendProducts,{
                                oisnlist: this.waitDeliverData.map(item => item.OIsn)
                            },{
                                params: {
                                    token: this.$common.getStore('token')
                                }
                            }).then(
                                res => {
                                    if (res.data.status == 200) {
                                        let resData = res.data,
                                            data = res.data.data;

                                        window.open(data);
                                        this.$notify({
                                            title: '订单导出成功',
                                            message: `请注意浏览器拦截,注意保存`,
                                            type: 'success'
                                        });
                                    }
                                }
                            )
                        }
                    )
                }else{
                    this.$message.warning('请勾选待发货的订单!');
                }
            },


            handleSelectionChange(val){
                this.waitDeliverData = val;
            },

            statusToTxt(status) {
                return this.statusOptions.find(item => item.value == status).label;
            }
        },

        activated(){
            this.setOrderList();
        },

        created() {
            this.setOrderList();
        },
    }
</script>

