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
            <!--<el-tree :data="data5" show-checkbox node-key="id" default-expand-all :expand-on-click-node="false">-->
                      <!--<span class="custom-tree-node" slot-scope="{ node, data }">-->
                        <!--<span>{{ node.label }}</span>-->
                        <!--<span>-->
                          <!--<el-button type="text" size="mini" @click="() => append(data)">-->
                            <!--Append-->
                          <!--</el-button>-->
                          <!--<el-button type="text" size="mini" @click="() => remove(node, data)">-->
                            <!--Delete-->
                          <!--</el-button>-->
                        <!--</span>-->
                      <!--</span>-->
            <!--</el-tree>-->

            <el-col :span="14">

                <el-tree :data="treeData" :props="treeProps" node-key="PAid" default-expand-all>

                 <span class="custom-tree-node" slot-scope="{ node, data }">
                     <span>{{ node.label}}</span>
                     <span v-if="node.label">
                          <el-button type="text" size="mini">
                                添加同级
                          </el-button>
                          <el-button type="text" size="mini">
                                添加子级
                          </el-button>
                         <el-button type="text" size="mini">
                                删除
                          </el-button>
                     </span>
                     <span v-else>
                         <el-button type="text" size="mini">
                                删除
                          </el-button>
                     </span>
                 </span>
                </el-tree>
            </el-col>
        </div>
    </div>
</template>

<script>
    let id = 1000;
    const data = [
        {
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
        name: "category",

        data() {
            return {
                data5: data,

                treeData: [],
                treeProps: {
                    value: 'PAid',
                    label: 'Parentname',
                    children: 'child_category',
                },

            }
        },

        components: {},

        computed: {},

        methods: {
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

            setCategoryList() {
                this.$http.get(this.$api.getProductCategoryList).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.treeData = data;
                        }
                    }
                )
            },
        },

        created() {
            this.setCategoryList();
        },
    }
</script>

