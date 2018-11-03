<template>
  <div class="navbar" >
    <!--<svg t="1492500959545" @click="sidebar()" class="hamburger" :class="{'is-active':isActive}" style="" viewBox="0 0 1024 1024"-->
         <!--version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1691" xmlns:xlink="http://www.w3.org/1999/xlink" width="24" height="24">-->
      <!--<path d="M966.8023 568.849776 57.196677 568.849776c-31.397081 0-56.850799-25.452695-56.850799-56.850799l0 0c0-31.397081 25.452695-56.849776 56.850799-56.849776l909.605623 0c31.397081 0 56.849776 25.452695 56.849776 56.849776l0 0C1023.653099 543.397081 998.200404 568.849776 966.8023 568.849776z"-->
            <!--p-id="1692"></path>-->
      <!--<path d="M966.8023 881.527125 57.196677 881.527125c-31.397081 0-56.850799-25.452695-56.850799-56.849776l0 0c0-31.397081 25.452695-56.849776 56.850799-56.849776l909.605623 0c31.397081 0 56.849776 25.452695 56.849776 56.849776l0 0C1023.653099 856.07443 998.200404 881.527125 966.8023 881.527125z"-->
            <!--p-id="1693"></path>-->
      <!--<path d="M966.8023 256.17345 57.196677 256.17345c-31.397081 0-56.850799-25.452695-56.850799-56.849776l0 0c0-31.397081 25.452695-56.850799 56.850799-56.850799l909.605623 0c31.397081 0 56.849776 25.452695 56.849776 56.850799l0 0C1023.653099 230.720755 998.200404 256.17345 966.8023 256.17345z"-->
            <!--p-id="1694"></path>-->
    <!--</svg>-->

    <el-dropdown :hide-on-click="false" trigger="click" @command="handleCommand">
      <span><i class="icon-person-navbar icon"></i></span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item command="passward">修改密码</el-dropdown-item>
        <el-dropdown-item command="exit" divided>退出</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>

    <div class="m-modal" v-show="show_pwd_modal" @click="hideModal">
      <div class="m-modal-state">
        <div class="m-modal-content" @click="modalClick">
          <h3>管理员数据管理</h3>
          <p>--修改密码</p>
          <el-form :inline="false" :model="pwdForm" :rules="rules" ref="pwdForm"  label-width="1.2rem">
                <el-form-item label="请输入旧密码" prop="MApasswordOld">
                  <el-input v-model="pwdForm.MApasswordOld" type="password" class="m-input-pwd" placeholder=""></el-input>
                </el-form-item>
                <el-form-item label="请输入新密码" prop="MApasswordNew">
                  <el-input v-model="pwdForm.MApasswordNew" type="password" class="m-input-pwd" placeholder=""></el-input>
                </el-form-item>
                <el-form-item label="请确认新密码" prop="MApasswordRepeat">
                  <el-input v-model="pwdForm.MApasswordRepeat" type="password" class="m-input-pwd" placeholder=""></el-input>
                </el-form-item>
              <p class="m-btn-p" @click="pwdSubmit('pwdForm')">确认修改</p>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import store  from '../../../vuex/index.js';
  import api from '../../../api/api';
  import { MessageBox } from 'element-ui';
  import axios from 'axios';
export default {

  components: {

  },
  computed: {

  },
  data(){
    return{
      isActive:false,
      show_pwd_modal:false,
      pwdForm:{
        MApasswordOld:'',
        MApasswordNew:'',
        MApasswordRepeat:''
      },
      rules: {
        MApasswordOld: [
          { required: true, message: '请输入旧密码', trigger: 'blur' }
        ],
        MApasswordNew:[
          { required: true, message: '请输入新密码', trigger: 'blur' }
          ],
        MApasswordRepeat:[
          { required: true, message: '请确认新密码', trigger: 'blur' }
        ],
      }

    }
  },
  methods: {
    sidebar(v){
      store.state.isCollapse = !store.state.isCollapse;
      let main = document.getElementsByClassName("main-container")[0];
      if(store.state.isCollapse){
        main.style.marginLeft = '0.63rem';
        this.isActive = true;
      }else{
        main.style.marginLeft = '1.8rem';
        this.isActive = false;
      }

    },
    hideModal(){
      this.show_pwd_modal = false;
    },
    pwdSubmit(formName){
      let that = this;
      this.$refs[formName].validate((valid) => {
        if (valid) {
          axios.post(api.changePwd + '?token=' + that.$store.state.token,that.pwdForm).
          then(res=>{
            if(res.data.status == 200){
              this.$message({
                message: res.data.message,
                type: 'success'
              });
              this.show_pwd_modal = false;
              for(let i in that.pwdForm){
                that.pwdForm[i] = ''
              }
            }else{
              this.$message.error(res.data.message);
            }
          }, res=>{
            this.$message.error(res.data.message);
          });
        } else {
          console.log('error submit!!');
          return false;
        }
      });

    },
    handleCommand(command) {
      if(command == 'passward'){
        this.show_pwd_modal = true;
      }
    },
    modalClick(e){
      e.stopPropagation();
      return false
    }
  }
}
</script>

<style rel="stylesheet/less" lang="less" scoped>
  @import "../../../common/css/_variate";
  @import "../../../common/css/modal";
.navbar{
  /*height: 0.5rem;*/
  border: 1px solid @borderColor;
  display: flex;
  flex-flow: row;
  justify-content: flex-end;
  align-items: center;
  padding: 0.2rem;
  background-color: #5A738A;
  .m-search-box{
    width: 1.80rem;
    height: 0.27rem;
    line-height: 0.27rem;
    font-size: 0.12rem;
    border: 1px solid @mainColor;
    position: relative;
    border-radius: 5px;
    .icon-search{
      width: 0.18rem;
      height: 0.18rem;
      position: absolute;
      top: 0.05rem;
      left: 0.1rem;
      /*background: url("../../../common/images/icon-search.png");*/
      background-size: 100% 100%;
    }
    input{
      border: none;
      height: 0.27rem;
      width: 1.4rem;
      padding-left: 0.4rem;
      &:focus{
        border: none;
        outline-offset: 0;
        outline-color:transparent;
      }
    }
  }
  .icon{
    display: inline-block;
    width: 0.3rem;
    height: 0.3rem;
  }
  .icon-person-navbar{
      background: url("../../../common/images/icon-person-navbar.png");
    background-size: 100% 100%;
    margin: 0 0.05rem;
  }
  .icon-message{
    /*background: url("../../../common/images/icon-message.png");*/
    background-size: 100% 100%;
    margin: 0 0.2rem;
  }
  .navbar-sidebar{
    display: inline-block;
    width: 0.4rem;
    height: 0.4rem;
    cursor: pointer;
  }
}
  .hamburger.is-active {
    -webkit-transform: rotate(90deg);
    transform: rotate(90deg);
  }
  .hamburger {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
.m-modal{
  .m-modal-state{
    width: 4rem;
    height: 350px;
    text-align: center;
    p{
      font-size: 0.12rem;
      margin-bottom: 0.2rem;
    }
    .m-btn-p{
      font-size: 0.14rem;
      cursor: pointer;
    }
  }
}

</style>
