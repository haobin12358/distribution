<template>
  <div class="app-wrapper" >
    <!--<div v-if="device==='mobile'&&sidebar.opened" class="drawer-bg" @click="handleClickOutside"></div>-->
    <sidebar class="sidebar-container"></sidebar>
    <div class="main-container">
      <!--<navbar></navbar>-->
      <!--<tags-view></tags-view>-->
      <app-main></app-main>
    </div>
  </div>

</template>
<script type="text/ecmascript-6">
  import AppMain from './component/appMain.vue';
  import sidebar from './component/sidebar';
  import navbar from './component/Navbar';
    export default {
        data() {
            return {}
        },
      components: {
        AppMain,
        sidebar,
        navbar
      },
        methods: {},
        created() {

        }
    }
</script>
<style lang="less" rel="stylesheet/less" scoped>
  @import "../../common/css/_variate";
  .app-wrapper{
    min-height: 100%;
  }
.sidebar-container{
  /*-webkit-transition: width 0.28s;*/
  /*transition: width 0.28s;*/
  width: @sidebarWidth;
  height: 100%;
  position: fixed;
  font-size: 0;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 1001;
  overflow: auto;
  background-color: @blueyGrey;
  color: #e0e0e0;
}
  .main-container{
    min-height: 100%;
    -webkit-transition: margin-left 0.28s;
    transition: margin-left 0.28s;
    margin-left: @sidebarWidth;
  }
  /*滚动条样式*/
  .sidebar-container::-webkit-scrollbar {/*滚动条整体样式*/
    width: 0;     /*高宽分别对应横竖滚动条的尺寸*/
    height: 0;
  }
  .sidebar-container::-webkit-scrollbar-thumb {/*滚动条里面小方块*/
    border-radius: 5px;
    -webkit-box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
    background: rgba(0,0,0,0.2);
  }
  .sidebar-container::-webkit-scrollbar-track {/*滚动条里面轨道*/
    -webkit-box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
    border-radius: 0;
    background: rgba(0,0,0,0.1);
  }
</style>
