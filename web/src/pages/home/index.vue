<style lang="less" rel="stylesheet/less" scoped>
  @import "../../common/css/index";

</style>

<template>
  <div>
  </div>
</template>

<script>
  import {Toast} from "mint-ui"

  export default {
    name: "index",

    data() {
      return {}
    },

    components: {},

    methods: {},

    mounted(){
      this.$toast({
        message: 'success',
        iconClass: 'm-toast-success'
      })
    }
  }
</script>

