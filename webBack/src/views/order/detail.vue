<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .row-tow {
            .fj();
            margin-bottom: .3rem;

            .order-detail {
                border: 1px dotted grey;
                border-radius: .1rem;
                .wl(5.2rem, 3.2rem);
                margin-right: .2rem;
                padding: 0 .3rem;
                .fz(.2rem);

                .detail-item {

                }
            }
            .order-action-block {
                border: 1px dotted grey;
                border-radius: .1rem;
                flex: 1;
                height: 3.2rem;
                padding: .3rem;
                box-sizing: border-box;
            }

        }

        .table-pd {
            width: 100%;
            border: 1px dotted grey;
            border-radius: .1rem;
        }
    }
</style>

<template>
    <div class="container">
        <el-breadcrumb style="margin-bottom: .2rem;" separator-class="el-icon-arrow-right">
            <el-breadcrumb-item to="index" replace>所有订单</el-breadcrumb-item>
            <el-breadcrumb-item>订单详情</el-breadcrumb-item>
        </el-breadcrumb>

        <section class="tool-tip-wrap">
            <el-steps :active="order.OIstatus" align-center>
                <el-step title="待发货" description="请填写快递信息"></el-step>
                <el-step title="已发货" description="已填写快递信息"></el-step>
                <el-step title="已完成" description="发货后10天自动完成"></el-step>
            </el-steps>
        </section>

        <section class="row-tow">
            <section class="order-detail">
                <p class="detail-item">
                    <span class="label">订单号:</span>
                    <span class="value">{{order.OIsn}}</span>
                </p>

                <p class="detail-item">
                    <span class="label">总价:</span>
                    <span class="value">￥ {{order.OImount}}</span>
                </p>
                <p class="detail-item">
                    <span class="label">下单时间:</span>
                    <span class="value">{{order.OIcreatetime}}</span>
                </p>
                <p class="detail-item">
                    <span class="label">收件人:</span>
                    <span class="value">{{order.username}}</span>
                </p>
                <p class="detail-item">
                    <span class="label">手机号:</span>
                    <span class="value">{{order.userphonenum}}</span>
                </p>
                <p class="detail-item">
                    <span class="label">收货地址:</span>
                    <span
                        class="value">{{`${order.provincename} ${order.cityname} ${order.areaname} ${order.details}`}}</span>
                </p>

            </section>
            <section class="order-action-block">
                <el-form ref="formExpress" :rules="rules" :model="formExpress" label-position="left" size="medium">
                    <el-form-item prop="expressname" label="快递公司">
                        <el-select v-model="formExpress.expressname" placeholder="请选择">
                            <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item prop="expressnum" label="快递单号">
                        <el-col :span="14">
                            <el-input v-model="formExpress.expressnum" :readonly="order.OIstatus == 3"></el-input>
                        </el-col>

                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="doDeliver" v-if="order.OIstatus == 1 ">确定发货</el-button>
                        <el-button type="primary" @click="doDeliver" v-if="order.OIstatus == 2 ">修改发货信息</el-button>
                    </el-form-item>
                </el-form>
            </section>

        </section>
        <h1 class="my-title">
            发货清单
        </h1>
        <el-table :data="order.product_list" size="small" cell-class-name="primary-cell" stripe style="width: 100%">
            <el-table-column prop="img" align="center" label="图片" width="180">
                <template slot-scope="scope">
                    <img v-lazy="scope.row.PRimage" class="table-pic" alt="">
                </template>
            </el-table-column>
            <el-table-column prop="PRname" align="center" label=" 商品名" width="220"></el-table-column>
            <el-table-column prop="PRprice" align="center" label="单价" width="120"></el-table-column>
            <el-table-column prop="colorname" align="center" label="颜色" width="120"></el-table-column>
            <el-table-column prop="sizename" align="center" label="尺码" width="120"></el-table-column>
            <el-table-column prop="number" align="center" label="数量" width="120"></el-table-column>
        </el-table>
    </div>
</template>

<script>
    export default {
        name: "detail",

        data() {
            return {
                order: {},
                tableData2: [
                    {
                        img: '/static/images/test_img.png',
                        name: '纸尿裤',
                        price: 123,
                        num: 1,
                    }, {
                        img: '/static/images/test_img.png',
                        name: '纸尿裤',
                        price: 123,
                        num: 1,
                    }, {
                        img: '/static/images/test_img.png',
                        name: '纸尿裤',
                        price: 123,
                        num: 1,
                    }, {
                        img: '/static/images/test_img.png',
                        name: '纸尿裤',
                        price: 123,
                        num: 1,
                    }, {
                        img: '/static/images/test_img.png',
                        name: '纸尿裤',
                        price: 123,
                        num: 1,
                    },
                ],

                formExpress: {
                    expressname: '',
                    expressnum: ''
                },

                rules: {
                    expressname: [
                        {required: true, message: '请选择快递公司', trigger: 'blur'},
                    ],
                    expressnum: [
                        {required: true, message: '请输入快递单号', trigger: 'blur'},
                    ],
                },

                options: [
                    {
                        label: '顺丰快递',
                        value: '顺丰快递'
                    }, {
                        label: '邮政EMS',
                        value: '邮政EMS'
                    }, {
                        label: '中通快递',
                        value: '中通快递'
                    }, {
                        label: '韵达快递',
                        value: '韵达快递'
                    }, {
                        label: '圆通快递',
                        value: '圆通快递'
                    }, {
                        label: '申通快递',
                        value: '申通快递'
                    }, {
                        label: '百世快递',
                        value: '百世快递'
                    }, {
                        label: '天天快递',
                        value: '天天快递'
                    }, {
                        label: '其他快递',
                        value: '其他快递'
                    },
                ],
                value: '',
            }
        },

        components: {},

        computed: {},

        methods: {
            doDeliver() {
                this.$refs.formExpress.validate(
                    vaild => {
                        if (vaild) {
                            this.$confirm(`快递公司:${ this.formExpress.expressname} 快递单号:${this.formExpress.expressnum}`
                                , '确认').then(
                                () => {
                                    this.$http.post(this.$api.updateOrder, {
                                            "oisn": this.order.OIsn,
                                            "expressname": this.formExpress.expressname,
                                            "expressnum": this.formExpress.expressnum
                                        }, {
                                            params: {
                                                token: this.$common.getStore('token')
                                            }
                                        }
                                    ).then(
                                        res => {
                                            if (res.data.status == 200) {
                                                let resData = res.data,
                                                    data = res.data.data;

                                                this.order = data;
                                                this.$notify({
                                                    title: '发货成功',
                                                    message: `订单号:${this.order.OIsn}`,
                                                    type: 'success'
                                                });
                                            }
                                        }
                                    )
                                }
                            )
                        } else {
                            return
                        }
                    }
                )

            }
        },

        created() {
            this.order = this.$route.query;

            if (this.order.OIstatus == 4) {
                this.order.OIstatus = 1;
            }

            if (this.order.OIstatus != 1) {
                this.formExpress.expressname = this.order.expressname
                this.formExpress.expressnum = this.order.expressnum
            }

        },
    }
</script>

