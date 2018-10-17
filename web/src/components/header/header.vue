<style lang="less" scoped>
  @import "../../common/css/index";

</style>

<template>
  <div>
    <mt-header :title="title">
      <section v-if="showBack" slot="left" @click="goBack">
        <mt-button icon="back"></mt-button>
      </section>
      <section slot="right">
        <slot name="right"></slot>
      </section>
    </mt-header>
  </div>
</template>

<script>
  export default {
    name: "headerTop",

    props: ['title', 'showBack'],

    data() {
      return {}
    },

    components: {},

    methods: {
        goBack(){
            this.$router.back();
        }
    },
  }
</script>

