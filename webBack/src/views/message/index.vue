<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
    }
</style>

<template>
    <div class="container">
        <el-breadcrumb style="margin-bottom: .2rem;" separator-class="el-icon-arrow-right">
            <el-breadcrumb-item>公司消息</el-breadcrumb-item>
        </el-breadcrumb>
        <!--商品表格-->
        <el-table :data="tableData" v-loading="loading" stripe style="width: 100%">
            <el-table-column prop="CMtitle" label="标题" align="center" width="180"></el-table-column>
            <el-table-column prop="CMtype" label="类型" align="center" width="180">
                <template slot-scope="scope">
                    公告
                </template>
            </el-table-column>
            <el-table-column prop="CMfile" label="文件">
                <template slot-scope="scope">
                    <a :href="scope.row.CMfile" target="_blank">查看文件({{scope.row.CMfile | fileType}})</a>
                </template>
            </el-table-column>
            <el-table-column prop="CMdate" label="发布日期" align="center"></el-table-column>

            <el-table-column label="操作" width="120" fixed="right" :render-header="renderHeader">
                <template slot-scope="scope">
                    <!--<el-button type="text" size="small">编辑</el-button>-->
                    <el-button type="text" size="small" class="danger-text" @click="deleteMsg(scope.row)">删除</el-button>
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

        <el-dialog title="消息编辑" :visible.sync="dialogFormVisible" label-position="top">
            <el-form :model="form" :rules="rules">
                <el-form-item prop="title" label="标题">
                    <el-input v-model="form.title" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="消息类型">
                    <el-select v-model="form.type" placeholder="请选择活动区域">
                        <el-option label="公告" value="0"></el-option>
                        <!--<el-option label="区域二" value="beijing"></el-option>-->
                    </el-select>
                </el-form-item>
                <el-form-item label="消息文件">
                    <el-upload
                        class="upload-demo"
                        :action="$api.uploadFile"
                        accept="image/*,application/pdf"
                        :on-preview="handlePreview"
                        :on-success="handleSuccess"
                        :on-remove="handleRemove"
                        :before-remove="beforeRemove"
                        :limit="1"
                        :on-exceed="handleExceed"
                        :file-list="form.url">
                        <el-button size="small" type="primary">点击上传</el-button>
                        <div slot="tip" class="el-upload__tip">只能上传1个文件，且不超过20M,格式只能为图片或者pdf</div>
                    </el-upload>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="doConfirm">保 存</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "index",

        data() {
            return {

                loading: false,
                total: 0,
                currentPage: 1,
                pageSize: 10,
                tableData: [],

                dialogFormVisible: false,
                form: {
                    title: '',
                    type: '0',
                    url: [],

                },
                rules: {
                    title: [
                        {required: true, message: '标题必填', trigger: 'blur'}
                    ]
                }
            }
        },

        filters: {
            fileType: function (value) {
                if (!value) return ''

                let dotIndex = value.lastIndexOf('.');

                return value.substr(dotIndex+1);
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

            deleteMsg(row){
                this.$confirm(`确定删除该消息(标题:${row.CMtitle})?`, '提示', {
                    type: 'warning'
                }).then(
                    ()=>{
                        this.$http.post(this.$api.deleteComMessage,
                            {
                                messageid: row.CMid
                            },{
                                params: {
                                    token: this.$common.getStore('token')

                                }
                            }).then(
                            res => {
                                if (res.data.status == 200) {
                                    let resData = res.data,
                                        data = res.data.data;


                                    this.setMessageList();
                                    this.$notify({
                                        title: '消息删除成功',
                                        message: `标题:${row.CMtitle}`,
                                        type: 'success'
                                    });
                                }
                            }
                        )
                    }
                )
            },

            sizeChange(pageSize) {
                this.pageSize = pageSize;
                this.currentPage = 1;

                this.setMessageList();
            },
            pageChange(page) {
                this.currentPage = page;
                this.setMessageList();
            },
            setMessageList() {
                this.loading = true;

                this.$http.get(this.$api.getComMessage, {
                    noLoading: true,
                    params: {
                        token: this.$common.getStore('token'),
                        page: this.currentPage,
                        count: this.pageSize,

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

            doConfirm() {
                if (this.form.type && this.form.url[0]) {
                    this.$http.post(this.$api.publishComMessage, {
                        "type": Number(this.form.type),
                        "title": this.form.title,
                        "url": this.form.url[0]
                    }, {
                        params: {
                            token: this.$common.getStore('token')
                        }
                    }).then(
                        res => {
                            if (res.data.status == 200) {
                                let resData = res.data,
                                    data = res.data.data;

                                this.setMessageList();
                                this.dialogFormVisible = false;
                                this.$notify({
                                    title: '消息发布成功',
                                    message: `标题:${this.form.title}`,
                                    type: 'success'
                                });
                            }
                        }
                    )
                }
            },

            handleRemove(file, fileList) {
                console.log(file, fileList);
            },
            handleSuccess(res, file, fileList) {
                console.log(res, file, fileList);
                this.form.url[0] = res.data;
            },

            handlePreview(file) {
                console.log(file);
            },
            handleExceed(files, fileList) {
                this.$message.warning(`当前限制选择 1 个文件`);
            },
            beforeRemove(file, fileList) {
                return this.$confirm(`确定移除 ${ file.name }？`);
            },

            // handleRemove(file, fileList) {
            //     console.log(file, fileList);
            // },
            // handlePictureCardPreview(file) {
            //     this.dialogImageUrl = file.url;
            //     this.dialogVisible = true;
            // },
        },

        created() {
            this.setMessageList();
        },
    }
</script>

