<style lang="less" scoped>
  @import "../../common/css/index";

</style>

<template>
  <div>
    <mt-header :title="title">
      <section slot="left" @click="$route.back()">
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

    props: ['title'],

    data() {
      return {}
    },

    components: {},

    methods: {},
  }
</script>

