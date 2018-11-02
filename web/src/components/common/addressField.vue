<style lang="less" scoped>
    @import "../../common/css/index";

    .address-field {
        .city-picker-popup {
            width: 100%;

            .city-picker-toolbar {
                .fj();
                padding: 10px 30px;

                button {
                    .bgw();
                    .sc(38px, #26b83a);

                    &.cancel-btn {
                        color: @lightFontColor;
                    }
                }
            }
        }
    }
</style>

<template>
    <section class="address-field">
        <mt-field label="省市区" placeholder="请选择省市区" v-model="city" :readonly="true"
                  :disableClear="true" @click.native="showCityPopup">
            <img src="/static/images/arrow_down.png" style="width: 16px;height: 14px;" alt="">
        </mt-field>

        <mt-popup class="city-picker-popup" position="bottom" v-model="cityPopupVisible">
            <mt-picker :slots="slots" defaultIndex="0" valueKey="name" @change="onValuesChange" :showToolbar="true">
                <section class="city-picker-toolbar">
                    <button class="cancel-btn" @click="cityPopupVisible= false">取消</button>
                    <button @click="confirmPickArea">确认</button>
                </section>
            </mt-picker>
        </mt-popup>
    </section>

</template>

<script>
    export default {
        name: "addressField",

        props: {
            defaultTxt: ''
        },
        data() {
            return {
                city: '',
                cityPopupVisible: false,
                allArea: [],
                slots: [
                    {
                        flex: 1,
                        values: [],
                        className: 'slot1',
                        textAlign: 'center'
                    }, {
                        divider: true,
                        content: '-',
                        className: 'slot2'
                    }, {
                        flex: 1,
                        values: [],
                        className: 'slot3',
                        textAlign: 'center'
                    }
                    , {
                        divider: true,
                        content: '-',
                        className: 'slot4'
                    }, {
                        flex: 1,
                        values: [],
                        className: 'slot5',
                        textAlign: 'center'
                    }
                ],
                pickAreaVal: []
            }
        },

        components: {},

        computed: {},

        methods: {
            onValuesChange(picker, values) {
                if (!values[0] || !this.allArea.length) {
                    return
                }
                //  数据没拿到
                let pickProvince = this.allArea.find(item => item.id == values[0].id);

                if (pickProvince) {
                    let citys = pickProvince.city.map(item => {
                        return {
                            id: item.id,
                            name: item.name,
                            area: item.area
                        }
                    })
                    picker.setSlotValues(1, citys);

                    if (values[1]) {
                        let pickCity = citys.find(item => item.id == values[1].id);

                        if (pickCity) {
                            picker.setSlotValues(2, pickCity.area)

                            this.pickAreaVal = values;
                        }
                    }
                }
            },
            confirmPickArea() {
                if (this.pickAreaVal[2] && this.pickAreaVal[2].id) {
                    this.formData.cityid = '';

                    this.formData.areaid = this.pickAreaVal[2].id;
                    this.city = this.pickAreaVal[0].name + ' ' + this.pickAreaVal[1].name + ' ' + this.pickAreaVal[2].name;
                    this.cityPopupVisible = false;
                } else if (this.pickAreaVal[1] && this.pickAreaVal[1].id) {
                    this.formData.areaid = '';

                    this.formData.cityid = this.pickAreaVal[1].id;
                    this.city = this.pickAreaVal[0].name + ' ' + this.pickAreaVal[1].name;
                    this.cityPopupVisible = false;
                }

            },
            initCityPicker() {
                this.allArea = JSON.parse(getStore(ALL_AREA));
                this.slots[0].values = this.allArea.map(item => {
                    return {
                        id: item.id,
                        name: item.name,
                    }
                });
                this.slots[2].values = this.allArea[0].city.map(item => {
                    return {
                        id: item.id,
                        name: item.name,
                    }
                });
                this.slots[4].values = this.allArea[0].city[0].area;
            },
            showCityPopup() {
                setTimeout(() => {
                    this.cityPopupVisible = true
                }, 300)
            },
            formDataCheck() {
                if (!this.formData.USname) {
                    return '请输入收件人';
                }
                if (!this.formData.USphonenum) {
                    return '请输入手机号';
                }
                if (!(this.formData.cityid || this.formData.areaid)) {
                    return '请选择省市县';
                }
                if (!this.formData.details) {
                    return '请输入详细地址';
                }

            },
        },

        created() {
            this.initCityPicker()

            if (this.defaultAddress) {
                this.isAdd = false;

                this.city = editAddress.provincename + ' ' + editAddress.cityname;
                if (editAddress.areaname) {
                    this.city += ' ' + editAddress.areaname;
                }
            } else {
            }
        },
    }
</script>

