<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .line {
            text-align: center;
            .fz(.3rem);
            font-weight: bold;
        }

        .sku-title {
            text-align: center;
            margin: 0;
            font-size: .26rem;
        }

        .input-new-tag {
            width: 150px;
            margin-left: 10px;
            vertical-align: bottom;
        }

        .pin-right-bottom {
            position: fixed;
            right: 3rem;
            bottom: 2rem;
            font-size: .22rem;

        }
    }
</style>

<template>
    <div class="container">
        <el-breadcrumb style="margin-bottom: .2rem;" separator-class="el-icon-arrow-right">
            <el-breadcrumb-item to="index" replace>所有商品</el-breadcrumb-item>
            <el-breadcrumb-item>商品编辑</el-breadcrumb-item>
        </el-breadcrumb>


        <el-row style="margin-top: .3rem;">
            <el-col :span="14">
                <el-form :model="formData" :rules="rules" label-position="left" ref="ruleForm" size="medium"
                         label-width="140px"
                         class="demo-ruleForm">
                    <el-form-item prop="prname" label="商品名">
                        <el-input v-model.trim="formData.prname"></el-input>
                    </el-form-item>
                    <el-form-item prop="prpic" label="商品图片(限一张)">
                        <el-upload
                            class="avatar-uploader"
                            :action="uploadUrl"
                            :show-file-list="false"
                            accept="image/*"
                            :on-success="handleAvatarSuccess"
                            :before-upload="beforeAvatarUpload"
                        >
                            <img v-if="imageUrl" v-lazy="imageUrl" class="avatar">
                            <i v-else class="el-icon-plus avatar-uploader-icon"></i>

                            <div slot="tip" class="el-upload__tip">
                                建议为方形,大小不要超过10M,上传成功后会显示,上传大图请耐心等待
                            </div>
                        </el-upload>
                    </el-form-item>
                    <el-form-item prop="sowingmap" label="商品详情轮播图(最多9张)">
                        <el-upload
                            class="swiper-uploader"
                            :action="uploadUrl"
                            accept="image/*"
                            list-type="picture-card"
                            :file-list="detailImgs"
                            :on-success="handleDetailImgsSuccess"
                            :on-preview="handlePictureCardPreview"
                            :before-upload="beforeDetailImgsUpload"
                            :on-remove="handleDetailImgsRemove"
                            :http-request="uploadDetailImgs"
                            :limit="9"
                            :multiple="true">
                            <i class="el-icon-plus"></i>
                            <div slot="tip" class="el-upload__tip">可多选,建议先单独上传主图!建议为方形,大小不要超过10M,上传成功后会显示,上传大图请耐心等待.</div>
                        </el-upload>
                    </el-form-item>
                    <el-form-item prop="paid" label="分类">
                        <el-cascader :options="options" :props="cascaderProps" v-model="selectedOption">
                        </el-cascader>
                    </el-form-item>
                    <el-form-item prop="proldprice" label="原价格">
                        <el-input v-model="formData.proldprice" type="number"></el-input>
                    </el-form-item>
                    <el-form-item prop="prprice" label="折后价格">
                        <el-input v-model="formData.prprice" type="number"></el-input>
                    </el-form-item>
                    <!--<el-form-item prop="prstock" label="库存">-->
                    <!--<el-input v-model="formData.prstock" type="number"></el-input>-->
                    <!--</el-form-item>-->
                    <el-form-item prop="prlogisticsfee" label="邮费(1件时生效)">
                        <el-input v-model="formData.prlogisticsfee" type="number"></el-input>
                    </el-form-item>
                    <el-form-item prop="prdiscountnum" label="返点件数">
                        <el-input v-model="formData.prdiscountnum" type="number"></el-input>
                    </el-form-item>

                    <section class="my-title">
                        商品销售属性
                    </section>
                    <el-collapse v-model="activeNames">
                        <el-collapse-item :title="`选择的颜色和尺码${isEdit? '---当前是编辑状态,谨慎减去在售的组合!':''}`" name="1">
                            <el-form-item label="选择颜色(从共用的勾选)">
                                <el-checkbox :indeterminate="isColorIndeterminate" v-model="checkAllColor"
                                             @change="handleCheckAllColorsChange">全选
                                </el-checkbox>
                                <div style="margin: 15px 0;"></div>
                                <el-checkbox-group v-model="checkedColors" @change="handleCheckedColorsChange">
                                    <el-checkbox v-for="color in allColorsName" :label="color" :key="color">
                                        {{color}}
                                    </el-checkbox>
                                </el-checkbox-group>
                                <el-input ref="inputColor" class="input-new-tag" v-if="inputColorVisible"
                                          v-model.trim="inputColorVal"
                                          size="small" @keyup.enter.native="addColor" @blur="inputColorVisible=false"
                                          placeholder="回车保存新的颜色"
                                >
                                </el-input>
                                <el-tooltip v-else class="item" effect="dark" content="点击后切换成输入框,不能重名!"
                                            placement="right">
                                    <el-button type="=primary" size="small" @click="showInputColor" icon="el-icon-plus">
                                        新增颜色
                                    </el-button>
                                </el-tooltip>
                            </el-form-item>

                            <el-form-item label="选择尺码(从共用的勾选)">
                                <el-checkbox :indeterminate="isSizeIndeterminate" v-model="checkAllSize"
                                             @change="handleCheckAllSizesChange">全选
                                </el-checkbox>
                                <div style="margin: 15px 0;"></div>
                                <el-checkbox-group v-model="checkedSizes" @change="handleCheckedSizesChange">
                                    <el-checkbox v-for="size in allSizesName" :label="size" :key="size">
                                        {{size}}
                                    </el-checkbox>
                                </el-checkbox-group>
                                <el-input
                                    ref="inputSize"
                                    class="input-new-tag"
                                    v-if="inputSizeVisible"
                                    v-model.trim="inputSizeVal"
                                    size="small"
                                    @keyup.enter.native="addSize"
                                    @blur="inputSizeVisible=false"
                                    placeholder="回车保存新的尺码"
                                >
                                </el-input>
                                <el-tooltip v-else class="item" effect="dark" content="点击后切换成输入框,不能重名!"
                                            placement="right">
                                    <el-button type="=primary" size="small" @click="showInputSize" icon="el-icon-plus">
                                        新增尺码
                                    </el-button>
                                </el-tooltip>
                            </el-form-item>
                        </el-collapse-item>
                    </el-collapse>
                    <el-form-item label="商品销售属性(颜色与尺码的组合,可将不需要的组合的库存置0)">
                        <el-table :data="skuTableData" size="medium" :span-method="objectSpanMethod" border
                                  style="width: 100%; margin-top: 20px;" empty-text="请在上方勾选颜色和尺码的组合后再来补全库存">
                            <el-table-column prop="colorname" align="center" label="颜色" width="180">
                            </el-table-column>
                            <el-table-column prop="sizename" align="center" label="尺码">
                            </el-table-column>
                            <el-table-column label="库存" align="center">
                                <template slot-scope="scope">
                                    <el-input type="number" v-model.number="scope.row.stock"
                                              placeholder="不需要的组合为0就行"></el-input>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-form-item>
                    <!--<section class="tool-tip-wrap">-->
                    <!--<el-form-item  label="已选规格-颜色">-->
                    <!--<el-tag closable>标签一</el-tag>-->
                    <!--<el-tag closable type="success">标签二</el-tag>-->
                    <!--<el-tag closable type="info">标签三</el-tag>-->
                    <!--<el-tag closable type="warning">标签四</el-tag>-->
                    <!--<el-tag closable type="danger">标签五</el-tag>-->
                    <!--</el-form-item>-->
                    <!--<el-collapse v-model="colorActiveNames">-->
                    <!--<el-collapse-item title="商品属性-颜色" name="1">-->
                    <!--<el-tag>标签一</el-tag>-->
                    <!--<el-tag>标签一</el-tag>-->
                    <!--<el-tag>标签一</el-tag>-->
                    <!--<el-tag>标签一</el-tag>-->
                    <!--<el-tag>标签一</el-tag>-->
                    <!--</el-collapse-item>-->
                    <!--</el-collapse>-->
                    <!--</section>-->

                    <el-form-item>
                        <el-button type="primary" @click="doSavePd" icon="el-icon-edit">{{isEdit ? '保存商品' : '新增商品'}}</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>

        <section class="tool-tip-wrap pin-right-bottom">
            <el-button type="primary" @click="doSavePd" icon="el-icon-edit">{{isEdit ? '保存商品' : '新增商品'}}</el-button>
        </section>

        <el-dialog :visible.sync="dialogVisible">
            <img width="100%" :src="dialogImageUrl" alt="">
        </el-dialog>
    </div>
</template>

<script>
    import lrz from "lrz"

    const numberReg = /^[0-9]+([.]{1}[0-9]+){0,1}$/;    //  正数
    const positiveNumberReg = /^([1-9]\d*)$/;   //  正整数
    const natureNumberReg = /^(\d*)$/;   //  自然数
    export default {
        name: "productEdit",

        data() {
            return {
                isEdit: false,

                detailImgs: [],
                dialogImageUrl: '',
                dialogVisible: false,

                imageUrl: '',
                keepImg: false,


                options: [],
                cascaderProps: {
                    value: 'PAid',
                    label: 'PAname',
                    children: 'child_category',
                },
                selectedOption: [],

                formData: {
                    prid: "",
                    paid: "",
                    prname: "",
                    prpic: "",
                    proldprice: "",
                    prprice: "",
                    prstock: "",
                    prlogisticsfee: "0",
                    prdiscountnum: "1",
                    prstatus: '1',
                    sowingmap: '',
                    skulist: [],
                },
                rules: {
                    required: [
                        {required: true, message: '必填', trigger: 'blur'}
                    ],
                    prname: [
                        {required: true, message: '商品名必填', trigger: 'blur'}
                    ],
                    prpic: [
                        {required: true, message: '商品图必传', trigger: 'change'}
                    ],
                    sowingmap: [
                        {required: true, message: '商品详情轮播必传', trigger: 'change'}
                    ],


                    paid: [
                        {required: true, message: '请选择分类', trigger: 'change'}
                    ],

                    proldprice: [
                        {required: true, message: '原价必填', trigger: 'blur'},
                        {pattern: numberReg, message: '价格需要是正数', trigger: 'change'},
                    ],
                    prprice: [
                        {required: true, message: '折扣价必填', trigger: 'blur'},
                        {pattern: numberReg, message: '价格需要是正数', trigger: 'change'},
                    ],
                    prlogisticsfee: [
                        {required: true, message: '运费必填(可为0)', trigger: 'blur'},
                        {pattern: numberReg, message: '运费需要是正数', trigger: 'change'},
                    ],
                    prdiscountnum: [
                        {required: true, message: '返点件数必填', trigger: 'blur'},
                        {pattern: numberReg, message: '返点件数需要是正数', trigger: 'change'},

                    ],
                },

                activeNames: [],

                //  颜色
                checkAllColor: false,
                isColorIndeterminate: false,
                allColors: [],
                allColorsName: [],
                checkedColors: [],
                inputColorVisible: false,
                inputColorVal: '',

                //  颜色
                checkAllSize: false,
                isSizeIndeterminate: false,
                allSizes: [],
                allSizesName: [],
                checkedSizes: [],
                inputSizeVisible: false,
                inputSizeVal: '',

                spanArr: [],
                pos: 0,
                // colorActiveNames: [],   //  显示共用的颜色属性
            }
        },

        watch: {
            selectedOption(val) {
                this.formData.paid = val[1];
            },
            detailImgs(val) {
                this.formData.sowingmap = val.map(item => item.url);
            }
        },

        components: {},

        computed: {
            uploadUrl() {
                return this.$api.uploadFile + localStorage.getItem('token');
            },
            skuTableData() {
                let res = []

                for (let i = 0; i < this.checkedColors.length; i++) {
                    for (let j = 0; j < this.checkedSizes.length; j++) {
                        res.push({
                            psid: '',
                            coid: this.allColors.find(item => item.COname == this.checkedColors[i]).COid,
                            colorname: this.checkedColors[i],
                            siid: this.allSizes.find(item => item.SIname == this.checkedSizes[j]).SIid,
                            sizename: this.checkedSizes[j],
                            stock: 0,
                        });

                        if (this.isEdit) {
                            let resLastItem = res[res.length - 1],
                                existSkuItem = this.formData.skulist.find(item => {
                                    return item.colorid == resLastItem.coid && item.sizeid == resLastItem.siid;
                                });

                            if (existSkuItem) {
                                resLastItem.psid = existSkuItem.PSid;
                                resLastItem.stock = existSkuItem.PSstock;
                            }
                        }
                    }
                }



                this.getSpanArr(res);
                return res
            }
        },

        methods: {
            //  颜色
            handleCheckAllColorsChange(val) {
                this.checkedColors = val ? this.allColorsName : [];
                this.isColorIndeterminate = false;
            },
            handleCheckedColorsChange(value) {
                let checkedCount = value.length;
                this.checkAllColor = checkedCount === this.allColors.length;
                this.isColorIndeterminate = checkedCount > 0 && checkedCount < this.allColors.length;
            },
            showInputColor() {
                this.inputColorVisible = true;
                this.$nextTick(_ => {
                    this.$refs.inputColor.focus();
                    // this.$refs.saveTagInput.$refs.input.focus();
                });
            },
            addColor() {
                if (this.allColors.find(item => item.COname == this.inputColorVal)) {
                    this.$message.warning('无法添加重复的颜色!');
                    return
                }

                this.$http.post(this.$api.addColor, {
                    colorname: this.inputColorVal
                }, {
                    params: {
                        token: this.$common.getStore('token')
                    }
                }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.setAllColors();
                            this.$notify({
                                title: '商品属性新增成功',
                                message: `颜色名:${this.inputColorVal}`,
                                type: 'success'
                            });


                            this.inputColorVal = '';
                            this.inputColorVisible = false;
                        }
                    }
                );
            },

            //  尺码
            handleCheckAllSizesChange(val) {
                this.checkedSizes = val ? this.allSizesName : [];
                this.isSizeIndeterminate = false;
            },
            handleCheckedSizesChange(value) {
                let checkedCount = value.length;

                this.checkAllSize = checkedCount === this.allSizes.length;
                this.isSizeIndeterminate = checkedCount > 0 && checkedCount < this.allSizes.length;
            },
            showInputSize() {
                this.inputSizeVisible = true;
                this.$nextTick(_ => {
                    this.$refs.inputSize.focus();
                });
            },
            addSize() {
                if (this.allColors.find(item => item.SIname == this.inputSizeVal)) {
                    this.$message.warning('无法添加重复的尺码!');
                    return
                }

                this.$http.post(this.$api.addSize, {
                    sizename: this.inputSizeVal
                }, {
                    params: {
                        token: this.$common.getStore('token')
                    }
                }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.setAllSizes();
                            this.$notify({
                                title: '商品属性新增成功',
                                message: `尺码名:${this.inputSizeVal}`,
                                type: 'success'
                            });

                            this.inputSizeVal = '';
                            this.inputSizeVisible = false;
                        }
                    }
                )


            },

            //  sku表格
            getSpanArr(data) {
                this.spanArr = [];
                this.pos = 0;

                for (var i = 0; i < data.length; i++) {
                    if (i === 0) {
                        this.spanArr.push(1);
                        this.pos = 0
                    } else {
                        // 判断当前元素与上一个元素是否相同
                        if (data[i].coid === data[i - 1].coid) {
                            this.spanArr[this.pos] += 1;
                            this.spanArr.push(0);
                        } else {
                            this.spanArr.push(1);
                            this.pos = i;
                        }
                    }
                }
            },
            objectSpanMethod({row, column, rowIndex, columnIndex}) {
                if (columnIndex === 0) {
                    const _row = this.spanArr[rowIndex];
                    const _col = _row > 0 ? 1 : 0;
                    return {
                        rowspan: _row,
                        colspan: _col
                    }
                }
            },


            //  商品主图multiple
            handleAvatarSuccess(res, file) {
                this.formData.prpic = res.data;
                this.imageUrl = URL.createObjectURL(file.raw);
            },
            beforeAvatarUpload(file) {
                const isLt15M = file.size / 1024 / 1024 < 10;

                if (!isLt15M) {
                    this.$message.error('上传商品图片大小不能超过 10MB!');
                }

                if (isLt15M) {
                    //  替换之前上传的
                    this.imageUrl = '';
                    //  删除之前上传的
                    this.clearUploadedImg();
                }

                return isLt15M;
            },
            //  清除已经上传到服务器的头像,移除后调删除接口节省空间
            clearUploadedImg() {
                if (this.formData.prpic) {
                    this.$http.post(this.$api.removeFile, {
                        url: this.formData.prpic.split('file/')[1]
                    }, {
                        noLoading: true,
                        params: {
                            token: this.$common.getStore('token')
                        }
                    }).then()
                }
            },

            //  详情轮播图
            //  预览图
            handlePictureCardPreview(file) {
                this.dialogImageUrl = file.url;
                this.dialogVisible = true;
            },
            handleDetailImgsRemove(file, fileList) {
                this.detailImgs = this.detailImgs.filter(
                    item => item.uid != file.uid
                );
            },
            beforeDetailImgsUpload(file) {
                const isLt15M = file.size / 1024 / 1024 < 10;

                if (!isLt15M) {
                    this.$message.error('上传轮播图片大小不能超过 10MB!');
                }

                return isLt15M;
            },
            handleDetailImgsSuccess(response, file, fileList) {
                console.log(response, file, fileList);
                return
                //  显示
                this.detailImgs = fileList.map(item => {
                    let res = {
                        name: item.name,
                        url: item.url,
                    }

                    if (item.response && item.response.data) {
                        //  替换掉blob
                        res.url = item.response.data;
                    }

                    return res;
                });
            },
            uploadDetailImgs(file){
                console.log(file);
                let formData = new FormData();

                formData.append('file', file.file)

                this.$http({
                    url: file.action,
                    params: {
                        token: this.$common.getStore('token')
                    },
                    method: 'post',
                    data: formData,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                }).then(
                    res => {
                        if(res.data.status == 200){
                            let resData = res.data,
                                data = resData.data;

                            this.detailImgs.push({
                                name: file.file.name,
                                url: data
                            })
                        }
                    }
                )

            },

            //  设置分类列表
            setCategoryList() {
                this.$http.get(this.$api.getProductCategoryList, {
                    params: {
                        token: this.$common.getStore('token')
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

            //  设置所有商品属性-颜色
            setAllColors() {
                this.$http.get(this.$api.getColor, {
                    noLoading: true,
                    params: {
                        token: this.$common.getStore('token')
                    }
                }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.allColors = data;
                            this.allColorsName = data.map(item => item.COname);
                        }
                    }
                )
            },

            //  设置所有商品属性-尺码
            setAllSizes() {
                this.$http.get(this.$api.getSize, {
                    noLoading: true,
                    params: {
                        token: this.$common.getStore('token')
                    }
                }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;

                            this.allSizes = data;
                            this.allSizesName = data.map(item => item.SIname);
                        }
                    }
                )
            },

            //  校验sku库存合法
            checkSkuData() {
                if (this.skuTableData.length) {
                    for (let i = 0; i < this.skuTableData.length; i++) {
                        let res = `${this.skuTableData[i].colorname} ${this.skuTableData[i].sizename} `

                        if (this.skuTableData[i].stock === undefined) {
                            return res + '库存必填!'
                        }
                        if (!natureNumberReg.test(this.skuTableData[i].stock)) {
                            return res + '库存要求为自然数!'
                        }
                    }
                } else {
                    return '请勾选想要的销售属性后填写组合的库存'

                }


                return
            },

            //  保存商品
            doSavePd() {
                this.$refs.ruleForm.validate(
                    valid => {
                        if (valid) {
                            let checkSkuDataMsg = this.checkSkuData();

                            if (checkSkuDataMsg) {
                                this.$message.warning(checkSkuDataMsg)
                                return
                            }

                            this.formData.skulist = this.skuTableData;

                            console.log(this.formData);
                            this.$http.post(this.$api.saveProduct, this.formData, {
                                params: {
                                    token: this.$common.getStore('token')
                                }
                            }).then(
                                res => {
                                    if (res.data.status == 200) {
                                        let resData = res.data,
                                            data = res.data.data;

                                        this.$router.back();
                                        this.$notify({
                                            title: '商品保存成功',
                                            message: `商品名:${this.formData.prname}`,
                                            type: 'success'
                                        });
                                    }
                                }
                            )
                        } else {
                            this.$message.warning('请根据校验信息完善表单!')
                        }
                    }
                )


            },
        },

        destroyed() {
            // this.clearUploadedImg();
        },

        created() {
            this.setCategoryList();

            this.setAllColors();
            this.setAllSizes();


            let editPd = this.$route.query.pd;

            if (editPd) {
                this.isEdit = true;

                this.$http.post(this.$api.getProductDetails, {
                    prid: editPd.PRid
                }, {
                    params: {
                        token: this.$common.getStore('token')
                    }
                }).then(
                    res => {
                        if (res.data.status == 200) {
                            let resData = res.data,
                                data = res.data.data;


                            this.formData.prid = editPd.PRid;
                            this.formData.paid = editPd.PAid;
                            this.formData.prname = editPd.PRname;
                            this.formData.prpic = editPd.PRpic;
                            this.formData.proldprice = editPd.PRoldprice;
                            this.formData.prprice = editPd.PRprice;
                            this.formData.prlogisticsfee = editPd.PRlogisticsfee;
                            this.formData.prdiscountnum = editPd.PAdiscountnum;
                            this.formData.prstatus = editPd.PRstatus;
                            this.formData.skulist = data.skulist;
                            this.formData.sowingmap = data.sowingmap;

                            this.imageUrl = editPd.PRpic;
                            this.detailImgs = data.sowingmap.map(item => {
                                return {
                                    url: item
                                }
                            });

                            this.selectedOption = [editPd.firstpaid.toString(), editPd.PAid.toString()];
                            // this.skuTableData = data.skulist;

                            for (let i = 0; i < data.skulist.length; i++) {
                                if (!this.checkedColors.find(item => item == data.skulist[i].colorname)) {
                                    this.checkedColors.push(data.skulist[i].colorname);
                                }

                                if (!this.checkedSizes.find(item => item == data.skulist[i].sizename)) {
                                    this.checkedSizes.push(data.skulist[i].sizename);
                                }
                            }
                        }
                    }
                )
            }else{
                this.activeNames = ['1'];
            }

        },
    }
</script>

