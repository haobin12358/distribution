<template>
  <div class="m-tab">
    <template v-for="(item,index) in tabs">
      <span>
          <span class="m-tab-link" :class="item.click?'active':''" @click="tabClick(index)">{{item.name}}</span>
          <span class="m-tab-line" v-if="index != tabs.length-1">/</span>
        </span>
    </template>
  </div>
</template>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {
                name: ''
            }
        },
      props:{
        tabs:{
          type:Array,
          default:null
        }
      },
        components: {},
        methods: {
          tabClick(index){
            if(this.tabs[index].click){
              return false;
            }
            this.$emit('tabClick',index);
          }
        },
        created() {

        }
    }
</script>
<style lang="less" rel="stylesheet/less" scoped>
  @import "../../common/css/_variate";
  .m-tab{
    font-size: 0.16rem;
    margin-bottom: 0.3rem;
    .m-tab-link{
      cursor: pointer;
      &.active{
        color: @greyColor;
      }
    }
    .m-tab-line{
      margin: 0 0.2rem;
    }
  }
</style>
