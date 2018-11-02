<template>
  <div class="m-page" :class="position" v-if="total > 0">
    <el-pagination layout="prev, pager, next" :page-count="total" @current-change="pageChange">
    </el-pagination>
  </div>
</template>

<script>
  export default {
    name: 'Pagination',
    data () {
      return {

      }
    },
    props:{
      total:{ type:Number, default:1 },
      position:{ type:String, default:'center' }
    },
    methods:{
      pageChange(v) {
        this.$emit('pageChange',v)
      }
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>
  @import "../../common/css/index";
  .m-page{
    margin-top: 0.3rem;
    &:after{
      display: block;
      content: '';
      clear: both;
    }
    .el-pagination{
      .flex-row(center);
    }
    &.right{
      .el-pagination{
        .flex-row(flex-end);
      }

    }
  }

</style>
