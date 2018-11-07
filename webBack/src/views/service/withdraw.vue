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
                <el-form-item label="用户名">
                    <el-input v-model="form.user" placeholder="用户名"></el-input>
                </el-form-item>
                <el-form-item label="手机号">
                    <el-input v-model="form.user" placeholder="手机号"></el-input>
                </el-form-item>

                <el-form-item label="提交时间">
                    <el-col :span="11">
                        <el-date-picker type="date" v-model="form.dateStart" placeholder="起始日期" style="width: 100%;"></el-date-picker>
                    </el-col>
                    <el-col class="middle-line" :span="2">-</el-col>
                    <el-col :span="11">
                        <el-date-picker type="date" v-model="form.dateEnd" placeholder="结束日期" style="width: 100%;"></el-date-picker>
                    </el-col>
                </el-form-item>

                <el-form-item label="状态">
                    <el-select v-model="form.region">
                        <el-option label="全部" value="all"></el-option>
                        <el-option label="待审核" value="shanghai"></el-option>
                        <el-option label="待打款" value="beijing"></el-option>
                        <el-option label="已打款" value="beijing1"></el-option>
                        <el-option label="未通过" value="beijing2"></el-option>
                    </el-select>
                </el-form-item>


                <el-form-item>
                    <el-button type="primary">查询</el-button>
                </el-form-item>
            </el-form>
        </section>

        <!--商品表格-->
        <el-table :data="tableData" size="mini" stripe style="width: 100%">
            <el-table-column prop="name" label="用户名" width="120"></el-table-column>
            <el-table-column prop="name" label="手机号" width="120"></el-table-column>
            <el-table-column prop="name" label="日期" width="120"></el-table-column>
            <el-table-column prop="type" label="提现方式" width="120"></el-table-column>
            <el-table-column prop="info" label="账号信息" ></el-table-column>
            <el-table-column label="操作" width="220" fixed="right">
                <template slot-scope="scope">
                    <el-button type="text" size="small">审核通过</el-button>
                    <el-button type="text" size="small">审核不通过</el-button>
                </template>
            </el-table-column>
        </el-table>

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
        name: "index",

        data() {
            return {
                tableData: [{
                    date: '2016-05-02',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1518 弄',
                    type: '支付宝',
                    info: '王富贵 15988888888'
                }, {
                    date: '2016-05-02',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1518 弄',
                    type: '支付宝',
                    info: '王富贵 15988888888'
                }, {
                    date: '2016-05-02',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1518 弄',
                    type: '支付宝',
                    info: '王富贵 15988888888'
                }, {
                    date: '2016-05-02',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1518 弄',
                    type: '支付宝',
                    info: '王富贵 15988888888'
                }, {
                    date: '2016-05-02',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1518 弄',
                    type: '支付宝',
                    info: '王富贵 15988888888'
                }, {
                    date: '2016-05-02',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1518 弄',
                    type: '支付宝',
                    info: '王富贵 15988888888'
                }, ],

                dialogFormVisible: false,
                form: {}
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

            handleRemove(file, fileList) {
                console.log(file, fileList);
            },
            handlePictureCardPreview(file) {
                this.dialogImageUrl = file.url;
                this.dialogVisible = true;
            }
        },

        created() {
        },
    }
</script>

