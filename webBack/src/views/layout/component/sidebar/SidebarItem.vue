<template>
  <div class="sidebar-li1">
    <template v-for="(items,index) in list">
      <el-submenu :index="items.MNurl" v-if="items.children.length >0" :key="items.MNname">
        <template slot="title">
          <i :class="items.MNicon" class="icon"></i>
          <span slot="title">{{items.MNname}}</span>
        </template>
        <template v-for="(item,i) in items.children">
          <router-link :to="items.MNurl+'/'+item.MNurl" :key="item.MNname">
            <el-menu-item :index="items.MNurl+'/'+item.MNurl">
              <i class="icon"></i>
              <span>{{item.MNname}}</span>
            </el-menu-item>
          </router-link>
        </template>
      </el-submenu>
      <router-link :to="items.MNurl" v-else>
        <el-menu-item :index="items.MNurl">
          <i :class="items.MNicon" class="icon"></i>
          <span slot="title">{{items.MNname}}</span>
        </el-menu-item>
      </router-link>
    </template>
  </div>
</template>
<script type="text/ecmascript-6">
  export default {
    name: 'SidebarItem',
    data() {
      return {};
    },
    props: {
      list: {
        type: Array
      }
    },
    methods: {
      sidebarClick(v) {
        this.$emit('sidebarClick', v);
      }

    },
    created() {
      // console.log(this.list)
    }
  };
</script>
<style lang="less" rel="stylesheet/less" scoped>
  @import "../../../../common/css/_variate";

  .sidebar-li1 {
    /*margin-bottom: 0.7rem;*/
    .el-menu-item {
      font-size: 0.21rem;
    }
    .icon {
      display: inline-block;
      width: 0.4rem;
      height: 0.25rem;
      margin-right: 0.2rem;
      background: none;
      &.icon-person-side {
        /*background: url("../../../../common/images/icon-person-side.png");*/
        background-size: 100% 100%;
      }
      &.icon-product {
        /*background: url("../../../../common/images/icon-product.png");*/
        background-size: 100% 100%;
      }
      &.icon-order {
        /*background: url("../../../../common/images/icon-order.png");*/
        background-size: 100% 100%;
      }
      &.icon-activity {
        /*background: url("../../../../common/images/icon-activity.png");*/
        background-size: 100% 100%;
      }
    }
    .sidebar-one-content {
      padding: 0.2rem 0.2rem;
      position: relative;
      text-align: inherit;
      cursor: pointer;
      transition: border-color .3s, background-color .3s, color .3s;
      &:hover {
        background-color: #1f2d3d;
      }
      span {
        vertical-align: middle;
      }
      .sidebar-icon {
        display: inline-block;
        width: 0.15rem;
        height: 0.15rem;
        border: 1px solid #eee;
        margin-right: 0.1rem;
        /*background: url("../../../../common/images/edit.png");*/
      }
      .sidebar-more {
        display: inline-block;
        width: 0.10rem;
        height: 0.10rem;
        margin-top: 0.04rem;
        position: absolute;
        top: 0.2rem;
        right: 0.2rem;
      }
      &:after {
        display: block;
        content: '';
        clear: both;
      }
    }

    ul {
      &:before {
        display: block;
        content: '';
        clear: both;
      }
      background-color: @sidebarChildColor;
      li {
        a {
          display: block;
          padding: 0.2rem 0;
          text-align: center;
          cursor: pointer;
          color: @sidebarFont;
          transition: border-color .3s, background-color .3s, color .3s;
          &:hover {
            background-color: #001528;
          }
        }
      }
    }
  }
</style>
