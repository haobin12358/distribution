<style lang="less" scoped>
    @import "../../common/css/index";

    .container {
        .invite-code-list {
            margin-top: 10px;

            .invite-code-item {
                .bgw();
                .bs(10px, 3px, 6px);
                padding: 25px;
                .fj();

                .invite-code-img {
                    .wl(100px, 100px);
                    margin-right: 40px;
                }

                .invite-remain {
                    flex: 1;
                    display: flex;
                    justify-content: space-between;
                    flex-direction: column;

                    .deadline {
                    }
                }

                .remove-btn {
                    align-self: center;
                    .wl(40px, 40px);
                }
            }
        }
    }
</style>

<template>
    <div class="container">
        <header-top :show-back="true">
            <section slot="right">
                <router-link to="/newInvite" tag="img" src="/static/images/add.png"
                             class="my-add-img"></router-link>
            </section>
        </header-top>

        <ul class="invite-code-list">
            <li class="invite-code-item" v-for="item,index in qrCodeList" @click="gotoInviteLink(item)">
                <vue-qr :text="generateCodeUrl(item)" :size="50" :margin="0" class="invite-code-img"></vue-qr>
                <section class="invite-remain">
                    <span class="deadline">有限期限：{{item.QRovertime}}</span>
                    <span class="residue-degree">可用次数：{{item.QRnumber}}</span>
                </section>

                <img src="/static/images/close.png" @click.stop="removeInvite(item)" alt="" class="remove-btn">
            </li>
        </ul>


    </div>
</template>

<script>
    import VueQr from 'vue-qr'
    import {getQrcode, deleteQrcode} from "src/api/api"


    export default {
        name: "wantInvite",

        data() {
            return {
                qrCodeList: []
            }
        },

        components: {VueQr},

        computed: {},

        methods: {
            setQrcodeList() {
                getQrcode().then(
                    resData => {
                        if (resData) {
                            this.qrCodeList = resData.data;
                        }
                    }
                )
            },
            generateCodeUrl(item) {
                return 'http://' + location.host + '/#/agentAgreement?QRid=' + item.QRid;
            },
            gotoInviteLink(item) {
                this.$router.push({
                    path: '/inviteLink?code=' + encodeURIComponent(this.generateCodeUrl(item)) + '& QRid=' + item.QRid
                });
            },
            removeInvite(item) {
                this.$messagebox.confirm('确定删除邀请链接吗?').then(
                    () => {
                        deleteQrcode(item.QRid).then(
                            resData => {
                                if (resData) {
                                    this.$toast('删除邀请链接成功');
                                    this.setQrcodeList();
                                }
                            }
                        )
                    }
                );
            }
        },

        created() {
            this.setQrcodeList();
        },
    }
</script>

