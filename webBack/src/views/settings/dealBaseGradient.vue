<style lang="less" scoped>
    @import "../../common/css/index";

    .container {


        .action-wrap{
            .fj(center);
            margin-top: .4rem;

            .el-button{
                .fz(.26rem);
                margin-right: .5rem;
            }

        }
    }
</style>

<template>
    <div class="container">
        <el-table :data="tableData" v-loading="loading" size="medium" cell-class-name="primary-cell" stripe
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
                    <el-button type="text" size="small" @click="editHandler(scope.row)">编辑</el-button>
                    <el-button type="text" class="danger-text" size="small" @click="removeHandler(scope.row, scope)">
                        删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

        <el-dialog :title="oldForm? '编辑梯度' : '新增梯度'" :modal="false" :visible.sync="dialogFormVisible" top="50vh">
            <el-form :model="form">
                <el-form-item v-if="oldForm" label="原梯度信息">
                    {{`件数:${oldForm.DRnumber},金额:${oldForm.DRmoney}`}}
                </el-form-item>
                <el-form-item label="件数:" :label-width="formLabelWidth">
                    <el-input v-model="form.DRnumber" type="number"></el-input>
                </el-form-item>
                <el-form-item label="金额:" :label-width="formLabelWidth">
                    <el-input v-model="form.DRmoney" type="number"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" v-if="oldForm" @click="editGradient">确 定</el-button>
                <el-button type="primary" v-else @click="insertGradient">确 定</el-button>
            </div>
        </el-dialog>

        <section class="my-title">
            最后所有梯度需用下方的保存按钮保存
        </section>
        <section class="action-wrap">
            <el-button type="info" @click="setData">重 置</el-button>
            <el-button type="primary" @click="doConfirm">保 存</el-button>

        </section>
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
                    DRnumber: '',
                    DRmoney: '',
                },

                oldForm: null,

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

                this.form.DRnumber = 0;
                this.form.DRmoney = 0;
                this.oldForm=null;

            },

            insertGradient() {
                if (!(this.form.DRnumber && this.form.DRmoney && this.form.DRnumber > 0 && this.form.DRmoney > 0)) {
                    this.$message.warning('请合理填写表单!')
                    return
                }
                if (this.tableData.find(item => item.DRnumber == this.form.DRnumber)) {
                    this.$message.warning('已有该梯度!');
                    return
                }

                this.tableData.push(
                    {
                        DRnumber: this.form.DRnumber,
                        DRmoney: this.form.DRmoney,
                    }
                );
                this.tableData = this.tableData.sort((a,b) => a.DRnumber - b.DRnumber);
                this.dialogFormVisible = false;
                //
                // if (!this.tableData.length) {
                //     this.tableData.push(
                //         {
                //             DRnumber: this.form.DRnumber,
                //             DRmoney: this.form.DRmoney,
                //         }
                //
                //     )
                //     this.dialogFormVisible = false;
                //     return
                // }
                //
                // for (let i = 0; i < this.tableData.length; i++) {
                //     if (i == this.tableData.length - 1) {
                //         this.tableData.push(
                //             {
                //                 DRnumber: this.form.DRnumber,
                //                 DRmoney: this.form.DRmoney,
                //             }
                //         )
                //         this.dialogFormVisible = false;
                //
                //         return
                //     }
                //     if (this.tableData[i].DRnumber < this.form.DRnumber && this.tableData[i + 1].DRnumber > this.form.DRnumber) {
                //          this.tableData.splice(i+1, 0, {
                //             DRnumber: this.form.DRnumber,
                //             DRmoney: this.form.DRmoney,
                //         })
                //         this.dialogFormVisible = false;
                //         return
                //     }
                // }
            },

            editHandler(item){
                this.form = {
                    DRnumber: item.DRnumber,
                    DRmoney: item.DRmoney,
                };
                this.oldForm = {
                    DRnumber: item.DRnumber,
                    DRmoney: item.DRmoney,
                };

                this.dialogFormVisible = true;
            },

            editGradient(){
                if (!(this.form.DRnumber && this.form.DRmoney && this.form.DRnumber > 0 && this.form.DRmoney > 0)) {
                    this.$message.warning('请合理填写表单!')
                    return
                }
                if (this.tableData.find(item => item.DRnumber == this.form.DRnumber) && this.form.DRnumber != this.oldForm.DRnumber) {
                    this.$message.warning('已有该梯度!');
                    return
                }

                if(this.form.DRnumber == this.oldForm.DRnumber){
                    let findIndex = this.tableData.findIndex(item => item.DRnumber == this.form.DRnumber);

                    this.tableData[findIndex].DRmoney = this.form.DRmoney;
                    this.dialogFormVisible = false;
                }else{
                    let findIndex = this.tableData.findIndex(item => item.DRnumber == this.oldForm.DRnumber);

                    this.tableData.splice(findIndex,1);
                    this.insertGradient();
                    this.dialogFormVisible = false;
                }
            },

            removeHandler(item, scope){
                this.tableData.splice(scope.$index,1);
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
            },

            doConfirm(){
                this.$confirm(`确定保存该梯度?`, '提示', {
                    type: 'info'
                }).then(
                    () => {
                        let ruler = this.tableData.map(item => {
                            return {
                                number: item.DRnumber,
                                money: item.DRmoney,
                            }
                        })

                        this.$http.post(this.$api.updateDiscountRuler,{
                            ruler
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
                                        title: '梯度保存成功',
                                        type: 'success'
                                    });
                                }
                            }
                        )
                    }
                )
            },
        },

        created() {
            this.setData();
        },
    }
</script>

