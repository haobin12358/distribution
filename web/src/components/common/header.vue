<template>
  <div class="hello">
    <mt-header :title="$store.state.tabbar_select">
      <router-link to="/" slot="left">
        <mt-button icon="back"></mt-button>
      </router-link>
      <mt-button icon="more" slot="right"></mt-button>
    </mt-header>

  </div>
</template>

<script>
  export default {

    data () {
      return {

      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less" rel="stylesheet/less">
  @import "../../common/css/index";


</style>

