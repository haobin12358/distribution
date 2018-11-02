<template>
  <div>
    <!--<router-link to="/index/adminIndex" key="user">-->
        <div class="m-system-name" >
          <p class="m-system-p">积分红包后台管理系统</p>
        </div>
    <!--</router-link>-->
    <el-menu  class="el-menu-vertical-demo m-sidebar"
              mode="vertical"
              :collapse="isCollapse"
              :show-timeout="0"
              :hide-timeout="0"
              text-color="#fff"
              active-text-color="#fff"
              unique-opened
              @open="handleOpen"
              @close="handleClose">
      <sidebar-item :list="side_list" ></sidebar-item>
    </el-menu>
    <!--<sidebar-item :list="side_list" ></sidebar-item>-->

    <div class="user-name m-ft-21 tc">{{$store.state.username}}</div>
  </div>
</template>

<script type="text/ecmascript-6">
  import SidebarItem from './SidebarItem';
  import sideList from '../../../../common/json/side';
  import store from '../../../../vuex/index';
    export default {
        data() {
            return {
              side_list:''
            }
        },
      components:{
        SidebarItem
      },
        methods: {
          sidebarClick(v){
            console.log(v)
            this.side_list[v].opened = !this.side_list[v].opened;
            for(let i =0;i<this.side_list.length;i++){
              if(i != v){
                this.side_list[i].opened = false;
              }
            }
          },
          handleOpen(key, keyPath) {
            console.log(key, keyPath);
          },
          handleClose(key, keyPath) {
            console.log(key, keyPath);
          }
        },
        created() {
            if(this.$store.state.side == null){
              this.side_list = sideList.side;

            }else{
              this.side_list = this.$store.state.side;
              console.log(this.side_list)
            }
        },
        computed:{
          isCollapse() {
            return store.state.isCollapse
          }
        }
    }
</script>
<style lang="less" rel="stylesheet/less" scoped>
.m-system-name{
  font-size: 0.2rem;
  padding: 0.2rem 0;
  border-bottom: 1px solid #ffffff;
  margin: 0.2rem;
  text-align: center;
  color: #fff;
  cursor: pointer;
  .m-system-p{
    font-size: 0.3rem;
    letter-spacing: 1.5px;
  }
}
  .user-name {
    color: #fff;
    width: 2.6rem;
    height: 0.7rem;
    line-height: 0.7rem;
    background-color: #9ca8ac;
    position: fixed;
    left: 0;
    bottom: 0;
  }
</style>
