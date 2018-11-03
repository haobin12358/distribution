<template>
  <div class="login-status">
    <!--<login-head></login-head>-->
    <div class="login-content">
      <div class="login-box">
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm"  >
          <h3 class="login-head">忘记密码</h3>
          <!--<el-form-item  prop="name">-->
            <!--<i class="icon-person icon"></i>-->
            <!--<el-input v-model="ruleForm.MAname" placeholder="输入账号/邮箱" class="m-input"></el-input>-->
          <!--</el-form-item>-->
          <el-form-item  prop="MAtelphone" label="手机号">
            <i class="icon-tel icon"></i>
            <el-input v-model="ruleForm.MAtelphone" placeholder="输入手机号" class="m-input"></el-input>
          </el-form-item>
          <el-form-item  prop="MAcode" label="验证码">
            <i class="icon-tel icon"></i>
            <el-input v-model="ruleForm.MAcode" placeholder="验证码" class="m-input-s m-input"></el-input>
            <span class="m-code" v-if="show" @click="getCode">获取验证码</span>
            <span class="m-code active" v-else >重发{{count}}s</span>
          </el-form-item>
          <el-form-item  prop="MApasswordnew" label="新密码">
            <span class="icon-pwd icon"></span>
            <el-input v-model="ruleForm.MApasswordnew" placeholder="输入新密码" type="password" class="m-input"></el-input>
            <!--<i class="icon-pwd icon-r"></i>-->
          </el-form-item>
          <el-form-item  prop="MApasswordnewrepeat" label="旧密码">
            <span class="icon-pwd icon"></span>
            <el-input v-model="ruleForm.MApasswordnewrepeat" placeholder="重复新密码" type="password" class="m-input"></el-input>
            <!--<i class="icon-pwd icon-r"></i>-->
          </el-form-item>
          <el-form-item class="m-btn">
            <el-button type="primary" @click="submitForm('ruleForm')">修&nbsp;改</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>

    <!--<foot></foot>-->
  </div>

</template>

<script>
  import api from '../../api/api';
  import { MessageBox } from 'element-ui';
  import axios from 'axios';
  export default {
    data() {
      return {
        ruleForm: {
          MAcode: '',
          MApasswordnew:'',
          MApasswordnewrepeat:'',
          MAtelphone:''
        },
        show:true,
        timer:null,
        count:'',
        rules: {
          MAcode: [
            { required: true, message: '请输入验证码', trigger: 'blur' }
          ],
          MApasswordnew:[
            { required: true, message: '请输入新密码', trigger: 'blur' }
          ],
          MApasswordnewrepeat:[
            { required: true, message: '请输入新密码', trigger: 'blur' }
          ],
          MAtelphone:[
            { required: true, message: '请输入手机号', trigger: 'blur' }
          ],
        }
      };
    },
    //页面加载调用获取cookie值
    mounted() {

    },
    methods: {
      submitForm(formName) {
        let that = this;
        this.$refs[formName].validate((valid) => {
          if (valid) {
            axios.post(api.forget_password,that.ruleForm).
            then(res=>{
              if(res.data.status == 200){
                this.$router.push('/login');
                //清空Cookie

                  let exdate = new Date(); //获取时间
                  exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * -1); //保存的天数
                  //字符串拼接cookie
                  window.document.cookie = "userName" + "=" + '' + ";path=/;expires=" + exdate.toGMTString();
                  window.document.cookie = "userPwd" + "=" + '' + ";path=/;expires=" + exdate.toGMTString();

              }else{
                MessageBox({
                  title:'提示',
                  message:res.data.message,
                  callback: action => {

                  }
                })
              }
            }, res=>{
              MessageBox({
                title:'提示',
                message:res.data.message,
                callback: action => {

                }
              })
            });
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      getCode(){
        if(this.ruleForm.MAtelphone == ''){
          this.$message.error('请先输入手机号');
          return false;
        }
        this.show = false;
        const TIME_COUNT = 60;
        axios.post(api.get_inforcode,{MAtelphone:this.ruleForm.MAtelphone}).then(res => {
          console.log(res)
        });
        if (!this.timer) {
          this.count = TIME_COUNT;
          this.show = false;
          this.timer = setInterval(() => {
            if (this.count > 0 && this.count <= TIME_COUNT) {
              this.count--;
            } else {
              this.show = true;
              clearInterval(this.timer);
              this.timer = null;
            }
          }, 1000)
        }
      }
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>
  @import "../../common/css/_variate";
  .login-status{
    height: 100%;
    .login-content{
      position: fixed;
      background: url("../../common/images/login-back.png");
      background-size: 100% 100%;
      width: 100%;
      height: 100%;
      .login-box{
        width: 3.6rem;
        /*height: 5.2rem;*/
        padding: 0.6rem;
        position: absolute;
        top: 35%;
        right: 1.2rem;
        background-color: #fff;
        -webkit-transform: translate(0, -1.6rem);
        transform: translate(0,-1.6rem);
        /*border-radius: 5px;*/
        .login-head{
          margin-bottom: 0.4rem;
          font-size: 0.25rem;
          color: @mainFont;
        }
        .el-form-item{
          vertical-align: middle;
          position: relative;
          /*height: 0.4rem;*/
          .m-input-s{
            width: 1.40rem;
          }
          .m-code{
            width: 1.4rem;
            height: 0.44rem;
            line-height: 0.44rem;
            text-align: center;
            display: inline-block;
            background-color: @btnActiveColor;
            color: #fff;
            /*border-radius: 5px;*/
            margin-left: 0.1rem;
            cursor: pointer;
            &.active{
              background-color: @btnColor;
              color: @greyColor;
              cursor: not-allowed;
            }
          }
          .icon{
            width: 0.25rem;
            height: 0.25rem;
            position: absolute;
            display: inline-block;
            top:0.145rem;
            left: 0.2rem;
            z-index: 100;
          }
          .icon-person{
            /*background: url("../../common/images/person.png");*/
            background-size: 100% 100%;
          }
          .icon-tel{
            /*background: url("../../common/images/icon-tel.png");*/
            background-size: 100% 100%;
          }
          .icon-r{
            width: 0.2rem;
            height: 0.2rem;
            position: absolute;
            display: inline-block;
            top:0.185rem;
            right: 0.1rem;
            z-index: 100;
          }
          .icon-pwd{
            /*background: url("../../common/images/pwd.png") no-repeat ;*/
            background-size: 100% 100%;
          }
          button{
            width: 3.6rem;
            height: 0.54rem;
            text-align: center;
            font-size: 0.2rem;
            background-color: @btnActiveColor;
            border-color: @btnActiveColor;
            border-radius: 0;
            /*margin-top: 1rem;*/
          }
          .m-forget-pwd{
            color: @greyColor;
            /*display: inline-block;*/
            position: absolute;
            top:0;
            right: 0;
            cursor: pointer;
          }
        }
      }
    }

  }

</style>
