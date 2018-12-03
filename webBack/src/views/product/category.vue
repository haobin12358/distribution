<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .custom-tree-node {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 14px;
            padding-right: 8px;
        }
    }
</style>

<template>
    <div class="container">
        <div class="block">

            <section class="tool-tip-wrap">
                <el-form :inline="true" size="small" ref="ruleForm" :rules="rules" :model="formInline"
                         class="demo-form-inline">
                    <el-form-item prop="PAname" label="分类名">
                        <el-input v-model.trim="formInline.PAname" :clearable="true" placeholder="分类名"></el-input>
                    </el-form-item>

                    <el-form-item label="分类类型">
                        <el-switch
                            v-model="isFirstLevel"
                            active-text="一级分类"
                            inactive-text="二级分类"
                            active-color="#13ce66"
                            inactive-color="#ff4949"
                            :disabled="!!formInline.PAid"
                        >
                        </el-switch>
                    </el-form-item>


                    <el-form-item prop="Parentid" label="所属分类" v-if="!isFirstLevel">
                        <el-cascader
                            :options="options"
                            :props="cascaderProps"
                            v-model="secondPAid"
                        >
                        </el-cascader>
                    </el-form-item>

                    <el-form-item>
                        <el-button v-if="!formInline.PAid" type="primary" icon="el-icon-plus" @click="doAdd">新 增
                        </el-button>
                        <el-button v-else type="primary" icon="el-icon-edit" @click="doEdit">编 辑</el-button>
                        <el-button  icon="el-icon-refresh" @click="doReset">重 置</el-button>
                    </el-form-item>
                </el-form>
            </section>
            <el-col :span="14" style="padding-bottom: 1rem;">
                <!--<el-button type="primary"  style="margin-bottom: .3rem;" @click="addFirstCategory">添加一级分类</el-button>-->
                <el-tree :data="treeData" :props="treeProps" node-key="PAid" default-expand-all
                         :expand-on-click-node="false" :highlight-current="true">

                 <span class="custom-tree-node" slot-scope="{ node, data }">
                     <span>{{ node.label}}</span>
                     <!--<span v-if="node.level == 1">-->
                     <!--<el-button type="text" size="mini" @click="addTwoLevelCategory(node,data)">-->
                     <!--添加二级分类-->
                     <!--</el-button>-->
                     <!--</span>-->
                     <el-button type="text" size="mini" @click="editCategory(node,data)">
                         编辑
                      </el-button>
                     <el-button type="text" class="danger-text" size="mini" @click="removeCategory(node,data)">
                         删除
                      </el-button>
                 </span>
                </el-tree>
            </el-col>
        </div>
    </div>
</template>

<script>
    export default {
        name: "category",

        data() {
            let paidValidator = (rule, value, callback) => {
                if (!this.isFirstLevel && !value) {
                    callback(new Error('所属一级分类必选'));
                } else {
                    callback();
                }
            };

            return {
                isFirstLevel: true,
                secondPAid: [],

                //  商品分类选项
                options: [],
                cascaderProps: {
                    value: 'PAid',
                    label: 'PAname',
                    children: 'child_category',
                },

                formInline: {
                    PAid: '',
                    PAname: '',
                    PAtype: '1',
                    Parentid: '',
                },

                rules: {
                    PAname: [
                        {required: true, message: '分类名称必填', trigger: 'blur'}
                    ],
                    Parentid: [
                        {validator: paidValidator, trigger: 'blur'}
                    ]


                },

                treeData: [],
                treeProps: {
                    value: 'PAid',
                    label: 'PAname',
                    children: 'child_category',
                },

            }
        },

        watch: {
            secondPAid(val) {
                if (val) {
                    this.formInline.Parentid = val[0];
                }
            }
        },

        components: {},

        computed: {},

        methods: {
            doAdd() {
                console.log(this.formInline);
                if (this.isFirstLevel) {
                    this.formInline.PAtype = 1;
                    this.formInline.Parentid = 0;
                } else {
                    this.formInline.PAtype = 2;
                    this.formInline.Parentid = this.secondPAid[0];
                }

                this.addCategory(this.formInline.PAname, this.formInline.PAtype, this.formInline.Parentid);
            },

            doEdit() {
                this.addCategory(this.formInline.PAname, this.formInline.PAtype, this.formInline.Parentid, this.formInline.PAid);
            },

            doReset() {
                this.formInline = {
                    PAname: '',
                    PAtype: '1',
                    Parentid: '',
                };
            },


            addCategory(PAname, PAtype, Parentid = 0, PAid = '') {
                this.$refs.ruleForm.validate(
                    valid => {
                        if(valid){
                            this.$http.post(this.$api.addProductCategory, {
                                PAid,
                                PAname,
                                PAtype,
                                Parentid
                            }, {
                                params: {
                                    token: this.$common.getStore('token')
                                }
                            }).then(
                                res => {
                                    if (res.data.status == 200) {
                                        let resData = res.data,
                                            data = res.data.data;

                                        this.setCategorySelect();
                                        this.setCategoryList();
                                        this.$notify({
                                            title: `商品分类${PAid ? '修改' : '新增'}成功`,
                                            message: `分类名:${PAname}`,
                                            type: 'success'
                                        });
                                    }
                                }
                            )
                        }else{
                            this.$message.warning('请根据校验信息完善表单!')

                        }
                    })

            },
            addFirstCategory() {

            },
            addTwoLevelCategory(node, data) {
                console.log('添加分类', node, data);
            },

            editCategory(node, data) {
                this.isFirstLevel = node.level == 1;

                this.formInline.PAid = data.PAid;
                this.formInline.PAname = data.PAname;
                this.formInline.PAtype = node.level;

                this.formInline.Parentid = node.parent.data.PAid ? node.parent.data.PAid : '';
                this.secondPAid = [this.formInline.Parentid.toString()];
            },
            removeCategory(node, data) {
                let PAname = data.PAname;

                if(this.formInline.PAid){
                    this.$message.warning('编辑中,请编辑完或点重置后再进行删除!')
                    return
                }

                if (node.childNodes.length) {
                    this.$message.error(`请先删除"${data.PAname}"下面的分类!`);
                } else {
                    this.$confirm(`确定要删除分类:${PAname}?`, '提示', {
                        type: 'warning'
                    }).then(
                        () => {
                            this.$http.post(this.$api.deleteCategory, {
                                PAid: data.PAid
                            }, {
                                params: {
                                    token: this.$common.getStore('token')

                                }
                            }).then(
                                res => {
                                    if (res.data.status == 200) {
                                        let resData = res.data,
                                            data = res.data.data;

                                        this.setCategorySelect();
                                        this.setCategoryList();
                                        this.$notify({
                                            title: `商品分类删除成功`,
                                            message: `分类名:${PAname}`,
                                            type: 'success'
                                        });
                                    }
                                }
                            )
                        }
                    )

                }
            },


            setCategoryList() {
                this.$http.get(this.$api.getProductCategoryList,{
                    params:{
                        token: this.$common.getStore('token')
                    }
                }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.treeData = data;
                        }
                    }
                )
            },
            setCategorySelect() {
                this.$http.get(this.$api.getProductCategory, {
                    params: {
                        PAtype: 1,
                        PAid: 0,
                    }
                }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.options = data;
                        }
                    }
                )
            },

        },

        created() {
            this.setCategoryList();
            this.setCategorySelect();
        },
    }
</script>

