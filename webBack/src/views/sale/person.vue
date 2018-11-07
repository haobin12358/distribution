<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .switch-month-row{
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

            <el-button type="primary">发放奖励</el-button>
            <el-button type="primary" disabled>奖励已发放/当月累加中</el-button>
        </section>

        <!--查询-->
        <section class="tool-tip-wrap">
            <el-form :inline="true" size="small" :model="formInline" class="demo-form-inline">
                <el-form-item label="用户名">
                    <el-input v-model="formInline.user" placeholder="用户名"></el-input>
                </el-form-item>
                <el-form-item label="手机号">
                    <el-input v-model="formInline.user" placeholder="手机号"></el-input>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary">查询</el-button>
                </el-form-item>
            </el-form>
        </section>

        <el-table :data="tableData" stripe style="width: 100%">
            <el-table-column prop="name" label="用户名" width="180"></el-table-column>
            <el-table-column prop="name" label="手机号" width="180"></el-table-column>
            <el-table-column label="直推奖励">
                <template slot-scope="scope">
                    <el-button type="text" size="small" @click="dialogTableVisible = true">{{scope.row.price}}
                    </el-button>
                </template>
            </el-table-column>
            <el-table-column label="销售折扣">
                <template slot-scope="scope">
                    <el-button type="text" size="small" @click="dialogTableVisible2 = true">{{scope.row.price}}
                    </el-button>
                </template>
            </el-table-column>
            <el-table-column prop="priceTotal" label="总奖金">
            </el-table-column>
        </el-table>

        <el-dialog title="直推奖励详情" :visible.sync="dialogTableVisible">
            <el-table :data="gridData">
                <el-table-column property="date" label="用户" width="150"></el-table-column>
                <el-table-column property="name" label="手机号" width="200"></el-table-column>
                <el-table-column property="address" label="注册时间"></el-table-column>
            </el-table>
        </el-dialog>
        <el-dialog title="销售折扣详情" :visible.sync="dialogTableVisible2">
            <el-table :data="gridData">
                <el-table-column property="date" label="用户" width="150"></el-table-column>
                <el-table-column property="name" label="手机号" width="200"></el-table-column>
                <el-table-column property="address" label="件数"></el-table-column>
                <el-table-column property="address" label="销售折扣"></el-table-column>
            </el-table>
        </el-dialog>



        <section style="display: flex; justify-content: center">
            <el-pagination
                style="margin-top: .5rem"
                :current-page="1"
                :page-sizes="[100, 200, 300, 400]"
                :page-size="100"
                layout="total, sizes, prev, pager, next, jumper"
                :total="400">
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

                formInline: {
                    user: '',
                    region: '',
                },

                tableData: [
                    {
                        date: '2016-05-02',
                        name: '王小虎',
                        address: '上海市普陀区金沙江路 1518 弄',
                        price: 100,
                        priceTotal: 200,
                    }, {
                        date: '2016-05-02',
                        name: '王小虎',
                        address: '上海市普陀区金沙江路 1518 弄',
                        price: 100,
                        priceTotal: 200,
                    }, {
                        date: '2016-05-02',
                        name: '王小虎',
                        address: '上海市普陀区金沙江路 1518 弄',
                        price: 100,
                        priceTotal: 200,
                    }, {
                        date: '2016-05-02',
                        name: '王小虎',
                        address: '上海市普陀区金沙江路 1518 弄',
                        price: 100,
                        priceTotal: 200,
                    },
                ],

                gridData: [{
                    date: '2016-05-02',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1518 弄'
                }, {
                    date: '2016-05-04',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1518 弄'
                }, {
                    date: '2016-05-01',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1518 弄'
                }, {
                    date: '2016-05-03',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1518 弄'
                }],
                dialogTableVisible: false,
                dialogTableVisible2: false,
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

            },
            nextMonth() {
                this.now = new Date(this.now).setDate(32);

            },
        },

        created() {
        },
    }
</script>

