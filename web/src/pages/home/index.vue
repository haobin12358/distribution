<style lang="less" rel="stylesheet/less" scoped>
  @import "../../common/css/index";

</style>

<template>
  <div>
    <header-top :title="'首页'"></header-top>
    <section>
      云仓
    </section>
    <footer-guide></footer-guide>
  </div>
</template>

<script>
  import {Toast} from "mint-ui"
  import headerTop from "src/components/header/header"
  import footerGuide from "src/components/footer/footerGuide"

  export default {
    name: "index",

    data() {
      return {}
    },

    components: {
      headerTop,
      footerGuide
    },

    methods: {},

    mounted(){
      // this.$toast({
      //   message: 'success',
      //   iconClass: 'm-toast-success',
      //   duration: 30000
      // })
    }
  }
</script>

