<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .big-size {
            font-size: .24rem;
        }
    }
</style>

<template>
    <div class="container">
        <el-table :data="tableData" v-loading="loading" cell-class-name="primary-cell" stripe
                  style="width: 100%">
            <el-table-column
                label="梯度"
                align="center"
                type="index"
                width="50">
            </el-table-column>
            <el-table-column prop="DRnumber" align="center" label="件数"></el-table-column>
            <el-table-column prop="DRmoney" align="center" label="金额"></el-table-column>

            <el-table-column label="操作" width="220" fixed="right" :render-header="renderHeader">
                <template slot-scope="scope">
                    <el-button type="text" size="small">编辑</el-button>
                    <el-button type="text" class="danger-text" size="small">
                        删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

        <el-dialog title="梯度" :visible.sync="dialogFormVisible">
            <el-form :model="form">
                <el-form-item label="件数" :label-width="formLabelWidth">
                    <el-input v-model="form.name"></el-input>
                </el-form-item>
                <el-form-item label="金额" :label-width="formLabelWidth">
                    <el-input v-model="form.name"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "dealBaseGradient",

        data() {
            return {
                loading: false,
                tableData: [],

                dialogFormVisible: false,
                form: {
                    name: '',
                    region: '',
                    date1: '',
                    date2: '',
                    delivery: false,
                    type: [],
                    resource: '',
                    desc: ''
                },
                formLabelWidth: '120px'
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

            doAddPd() {
                this.dialogFormVisible = true;
            },

            setData() {
                this.loading = true;
                this.$http.get(this.$api.getDiscountRuler, {
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

                            this.tableData = data;
                        }
                    }
                )
            }
        },

        created() {
            this.setData();
        },
    }
</script>

