<style lang="less" rel="stylesheet/less" scoped>
  @import "../../common/css/index";

  .tab-bar {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 88px;
    line-height: 88px;
    background: #ffffff;
    display: flex;
    text-align: center;

    .tab-bar-home {
      flex: .5;
      .m-flex-center();
      flex-direction: column;

      img {
        width: 32px;
        height: 32px;
      }
    }

    .tab-bar-item {
      flex: 1;
      border-left: 1px solid #a2a2a2;
    }
  }
</style>
<template>
  <div class="tab-bar">
    <template v-for="(item, index) in tabbar">
      <div v-if="index == 0" class="tab-bar-home" @click="selected = item.name">
        <img src="static/images/home.png"/>
      </div>
      <div v-else class="tab-bar-item" @click="selected = item.name">
        {{item.name}}
      </div>
    </template>
  </div>
</template>

<script type="text/ecmascript-6">
  import common from '../../common/js/common';

  export default {
    data() {
      return {
        name: '',
        selected: this.$store.state.tabbar[0].name,
        tabbar: this.$store.state.tabbar
      }
    },
    components: {},
    methods: {
      menuBarClick(v) {
        console.log(v)
      }
    },
    watch: {
      selected: function (val, oldVal) {
        console.log('[watch]', val);
        this.$store.state.tabbar_select = val;
        common.changeTitle(val);
        switch (val) {
          case '抢红包':
            this.$router.push('/home');
            break;
          case '积分商城':
            this.$router.push('/mall');
            break;
          case '在线客服':
            this.$router.push('/service');
            break;
          case '个人中心':
            this.$router.push('/personal');
            break;
        }
      }
    },
    created() {

    }
  }
</script>

