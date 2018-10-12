<template>
  <div class="m-content">
    <router-view ></router-view>
  </div>
</template>

<script type="text/ecmascript-6">
  export default {
    data() {
      return {
        name: ''
      }
    },
    components: {},
    methods: {},
    created() {

    }
  }
</script>
<style lang="less" rel="stylesheet/less">
.m-content{
  /*padding: 10px 0;*/
  margin-bottom: 120px;
}
</style>
