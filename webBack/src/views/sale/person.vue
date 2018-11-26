<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .switch-month-row {
            margin-bottom: .2rem;

            .fjc();
            align-items: center;
            .switch-month {
                .fj(center);
                align-items: center;
                margin-bottom: .2rem;

                .icon {
                    .wl(.4rem, .4rem);
                    cursor: pointer;
                }
                .txt {
                    .fz(.4rem);
                    font-weight: bold;
                    margin: 0 .3rem;
                }
            }
        }

    }
</style>

<template>
    <div class="container">
        <!--月度选择-->
        <section class="switch-month-row">
            <section class="switch-month">
                <img class="icon" @click="prevMonth" src="/static/images/arrow_left.png" alt="">
                <span class="txt">{{showMonth}}</span>
                <img class="icon" @click="nextMonth" src="/static/images/arrow_right.png" alt="">
            </section>

            <!--<el-button type="primary">发放奖励</el-button>-->
            <!--<el-button type="primary" disabled>奖励已发放/当月累加中</el-button>-->
        </section>

        <!--查询-->
        <section class="tool-tip-wrap">
            <el-form :inline="true" size="small" :model="formInline" class="demo-form-inline">
                <el-form-item label="用户名">
                    <el-input v-model="formInline.username" placeholder="用户名"></el-input>
                </el-form-item>
                <el-form-item label="手机号">
                    <el-input v-model="formInline.userphonenum" placeholder="手机号"></el-input>
                </el-form-item>
                <el-form-item label="代理号">
                    <el-input v-model="formInline.agentid" placeholder="代理号"></el-input>
                </el-form-item>


                <!--<el-form-item label="状态">-->
                    <!--<el-select v-model="formInline.status" @change="setSaleData">-->
                        <!--<el-option v-for="option in statusOptions" :label="option.label" :value="option.value"-->
                                   <!--:key="option.value">-->
                        <!--</el-option>-->
                    <!--</el-select>-->
                <!--</el-form-item>-->

                <el-form-item>
                    <el-button type="primary" icon="el-icon-search" @click="doSearch">查询</el-button>
                    <el-button @click="doReset" icon="el-icon-refresh">重置</el-button>
                </el-form-item>
            </el-form>
        </section>

        <el-table :data="tableData" v-loading="loading" stripe style="width: 100%">
            <el-table-column property="USagentid" align="center" label="代理号" width="150"></el-table-column>
            <el-table-column property="USname" align="center" label="用户名" width="150"></el-table-column>
            <el-table-column property="userphonenum" align="center" label="手机号" width="200"></el-table-column>
            <el-table-column label="直推奖励" align="center">
                <template slot-scope="scope">
                    <el-button type="text" size="small" @click="showZhiTuiDetail(scope.row)">
                        {{scope.row.reward}}
                    </el-button>
                </template>
            </el-table-column>
            <el-table-column label="销售折扣" align="center">
                <template slot-scope="scope">
                    <el-button type="text" size="small" @click="showDiscountDetail(scope.row)">{{scope.row.discount}}
                    </el-button>
                </template>
            </el-table-column>
            <el-table-column prop="myprofit" align="center" label="总奖金"></el-table-column>
            <!--<el-table-column prop="AMstatus" align="center" label="状态">-->
                <!--<template slot-scope="scope">-->
                    <!--<span v-if="scope.row.AMstatus == 1">未打款</span>-->
                    <!--<span v-if="scope.row.AMstatus == 2">已打款</span>-->
                    <!--<span v-if="scope.row.AMstatus == 3">累加中</span>-->
                <!--</template>-->
            <!--</el-table-column>-->
            <!--<el-table-column align="left" label="操作">-->
                <!--<template slot-scope="scope">-->
                    <!--<el-button type="text" size="mini" v-if="scope.row.AMstatus == 1" @click="grantReward(scope.row)">-->
                        <!--发放奖励-->
                    <!--</el-button>-->
                <!--</template>-->
            <!--</el-table-column>-->


        </el-table>

        <el-dialog title="直推奖励详情" :visible.sync="dialogTableVisible" width="60%">
            <el-table :data="rewardData" size="mini" style="width: 100%">
                <el-table-column prop="img" align="center" label="头像" width="120">
                    <template slot-scope="scope">
                        <img v-lazy="scope.row.USheadimg" class="table-pic"/>
                    </template>
                </el-table-column>
                <el-table-column property="USagentid" align="center" label="代理号" width="150"></el-table-column>
                <el-table-column property="USname" align="center" label="用户名"></el-table-column>
            </el-table>
        </el-dialog>
        <el-dialog title="销售折扣详情" :visible.sync="dialogTableVisible2" width="70%">
            <el-table :data="discountData" size="mini" style="width: 100%">
                <el-table-column prop="img" align="center" label="头像" width="120">
                    <template slot-scope="scope">
                        <img v-lazy="scope.row.USheadimg" class="table-pic"/>
                    </template>
                </el-table-column>
                <el-table-column property="USagentid" align="center" label="代理号" width="150"></el-table-column>
                <el-table-column property="USname" align="center" label="用户名"></el-table-column>
                <el-table-column property="performance" align="center" label="件数" width="150"></el-table-column>
            </el-table>
        </el-dialog>


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
        name: "person",

        data() {
            return {
                now: Date.now(),

                statusOptions: [
                    {
                        value: 0,
                        label: '全部',
                    }, {
                        value: 1,
                        label: '未打款',
                    }, {
                        value: 2,
                        label: '已打款',
                    },
                ],
                formInline: {
                    username: '',
                    userphonenum: '',
                    agentid: '',
                    status: 0,
                },

                loading: false,
                total: 0,
                currentPage: 1,
                pageSize: 10,
                tableData: [],

                dialogTableVisible: false,
                rewardData: [],

                dialogTableVisible2: false,
                discountData: [],

            }
        },

        components: {},

        computed: {
            showMonth() {
                let date = new Date(this.now);

                return date.getFullYear() + ' 年 ' + (date.getMonth() + 1) + ' 月';
            },
        },

        methods: {
            prevMonth() {
                this.now = new Date(this.now).setDate(-1);
                this.setSaleData();
            },
            nextMonth() {
                this.now = new Date(this.now).setDate(32);
                this.setSaleData();
            },

            doSearch() {
                this.setSaleData();
            },
            doReset() {
                this.formInline = {
                    username: '',
                    userphonenum: '',
                    agentid: '',
                    status: 0,
                }

                this.setSaleData();
            },

            sizeChange(pageSize) {
                this.pageSize = pageSize;
                this.currentPage = 1;

                this.setSaleData();
            },
            pageChange(page) {
                this.currentPage = page;
                this.setSaleData();
            },
            setSaleData() {
                this.loading = true;
                this.$http.post(this.$api.getAllUserAcount,
                    {
                        "month": this.$common.dateFormat(new Date(this.now)).substr(0, 6),

                        "username": this.formInline.username,
                        "userphonenum": this.formInline.userphonenum,
                        "status": this.formInline.status,
                        "agentid": this.formInline.agentid,

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

            showZhiTuiDetail(item) {
                this.dialogTableVisible = true;

                this.$http.post(this.$api.getDirectagentPerformance,
                    {
                        "usid": item.USid,
                        "month": this.$common.dateFormat(new Date(this.now)).substr(0, 6),
                    },
                    {
                        params: {
                            token: this.$common.getStore('token')

                        }
                    }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.rewardData = data;
                        }
                    }
                )
            },
            showDiscountDetail(item) {
                this.dialogTableVisible2 = true;

                this.$http.post(this.$api.getAllPerformance,
                    {
                        "usid": item.USid,
                        "month": this.$common.dateFormat(new Date(this.now)).substr(0, 6),
                    },
                    {
                        params: {
                            token: this.$common.getStore('token')

                        }
                    }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.discountData = data;
                        }
                    }
                )

            },


            grantReward(item) {
                console.log(item);
                this.$confirm(`确定发放该月奖励(用户名:${item.USname}),共${item.myprofit}元?`, '提示', {
                    type: 'info'
                }).then(
                    () => {
                        this.$http.post(this.$api.dealRewardDiscount, {
                            "amid": item.AMid,
                            "usid":  item.USid,
                            "month": this.$common.dateFormat(new Date(this.now)).substr(0, 6),
                            "profit": item.myprofit,
                        }, {
                            params: {
                                token: this.$common.getStore('token')

                            }
                        }).then(
                            res => {
                                if (res.data.status == 200) {
                                    let resData = res.data,
                                        data = res.data.data;

                                    this.setSaleData();
                                    this.$notify({
                                        title: '奖励发放成功',
                                        message: `用户名:${item.USname},共${item.myprofit}元`,
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
            this.setSaleData();
        },
    }
</script>

