<template>
    <div>
      <!--<m-header></m-header>-->
      <m-content></m-content>

      <m-footer></m-footer>
    </div>

</template>

<script type="text/ecmascript-6">
  import mHeader from '../../components/common/header';
  import mFooter from '../../components/common/footer';
  import mContent from './mContent';
    export default {
      data() {
        return {
          name: ''
        }
      },
      components: { mHeader, mFooter, mContent },
      methods: {},
      created() {

      }
    }
</script>
<style lang="less" rel="stylesheet/less" >

</style>
