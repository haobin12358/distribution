<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
    }
</style>

<template>
    <div class="container">
        <el-tabs v-model="activeName">
            <el-tab-pane label="所有商品" name="first">
                <el-form :inline="true" size="small" :model="formInline" class="demo-form-inline">
                    <el-form-item label="名称">
                        <el-input v-model="formInline.user" placeholder="商品名"></el-input>
                    </el-form-item>

                    <el-form-item label="分类">
                        <el-cascader
                            :options="options"
                            v-model="selectedOptions">
                        </el-cascader>
                    </el-form-item>
                    <el-form-item label="状态">
                        <el-select v-model="formInline.region">
                            <el-option label="全部" value="all"></el-option>
                            <el-option label="出售中" value="shanghai"></el-option>
                            <el-option label="已售罄" value="beijing"></el-option>
                            <el-option label="已下架" value="beijing1"></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item>
                        <el-button type="primary">查询</el-button>
                    </el-form-item>
                </el-form>

                <!--<div>-->
                <!--<el-button type="primary">新增</el-button>-->
                <!--<el-button type="primary">编辑</el-button>-->
                <!--</div>-->

                <el-table
                    :data="tableData" stripe style="width: 100%">
                    <el-table-column prop="name" label="商品名" width="180"></el-table-column>
                    <el-table-column prop="name" label="所属分类" width="180"></el-table-column>
                    <el-table-column prop="name" label="价格"></el-table-column>
                    <el-table-column prop="name" label="邮费"></el-table-column>
                    <el-table-column prop="name" label="返点件数"></el-table-column>
                    <el-table-column prop="name" label="创建时间"></el-table-column>

                    <el-table-column  label="操作" width="120" fixed="right" :render-header="renderHeader">
                        <template slot-scope="scope">
                            <el-button type="text" size="small">编辑</el-button>
                        </template>
                    </el-table-column>

                    <!--<el-table-column-->
                        <!--align="right">-->
                        <!--<template slot="header" slot-scope="slot">-->
                            <!--<el-button-->
                                <!--size="mini">Edit</el-button>-->
                        <!--</template>-->
                        <!--<template slot-scope="scope">-->
                            <!--<el-button-->
                                <!--size="mini">Edit</el-button>-->
                        <!--</template>-->
                    <!--</el-table-column>-->
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
            </el-tab-pane>
            <el-tab-pane label="商品分类" name="second">
                <div class="block">
                    <el-tree :data="data5" show-checkbox node-key="id" default-expand-all :expand-on-click-node="false">
                      <span class="custom-tree-node" slot-scope="{ node, data }">
                        <span>{{ node.label }}</span>
                        <span>
                          <el-button type="text" size="mini" @click="() => append(data)">
                            Append
                          </el-button>
                          <el-button type="text" size="mini" @click="() => remove(node, data)">
                            Delete
                          </el-button>
                        </span>
                      </span>
                    </el-tree>
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
    let id = 1000;
    const data = [{
        id: 1,
        label: '一级 1',
        children: [{
            id: 4,
            label: '二级 1-1',
            children: [{
                id: 9,
                label: '三级 1-1-1'
            }, {
                id: 10,
                label: '三级 1-1-2'
            }]
        }]
    }, {
        id: 2,
        label: '一级 2',
        children: [{
            id: 5,
            label: '二级 2-1'
        }, {
            id: 6,
            label: '二级 2-2'
        }]
    }, {
        id: 3,
        label: '一级 3',
        children: [{
            id: 7,
            label: '二级 3-1'
        }, {
            id: 8,
            label: '二级 3-2'
        }]
    }];

    export default {
        name: "index",

        data() {
            return {
                activeName: 'first',

                formInline: {
                    user: '',
                    region: 'all'
                },

                options: [
                    {
                        value: '0-1',
                        label: '上衣',
                        children: [{
                            value: '1-1',
                            label: '短袖',
                        }, {
                            value: '1-2',
                            label: '卫衣',
                        }, {
                            value: '1-3',
                            label: '衬衫',
                        },]
                    }, {
                        value: '0-2',
                        label: '下装',
                        children: [{
                            value: '1-1',
                            label: '短裤',
                        }, {
                            value: '1-2',
                            label: '长裤',
                        },]
                    },
                ],
                selectedOptions: '',


                tableData: [{
                    date: '2016-05-02',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1518 弄'
                }, {
                    date: '2016-05-04',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1517 弄'
                }, {
                    date: '2016-05-01',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1519 弄'
                }, {
                    date: '2016-05-03',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1516 弄'
                }, {
                    date: '2016-05-04',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1517 弄'
                }, {
                    date: '2016-05-01',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1519 弄'
                }, {
                    date: '2016-05-03',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1516 弄'
                }, {
                    date: '2016-05-01',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1519 弄'
                }, {
                    date: '2016-05-03',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1516 弄'
                }],
                search: '',

                data5: JSON.parse(JSON.stringify(data))



            }
        },

        components: {},

        computed: {},

        methods: {
            renderHeader(h) {
                return (
                    <router-link tag="el-button" to="productEdit" type="primary">
                            新增
                    </router-link>

            )
            },
            handleEdit(){},
            handleDelete(){},

            append(data) {
                const newChild = {id: id++, label: 'testtest', children: []};
                if (!data.children) {
                    this.$set(data, 'children', []);
                }
                data.children.push(newChild);
            },

            remove(node, data) {
                const parent = node.parent;
                const children = parent.data.children || parent.data;
                const index = children.findIndex(d => d.id === data.id);
                children.splice(index, 1);
            },
        },

        created() {
        },
    }
</script>

