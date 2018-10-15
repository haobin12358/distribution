<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100%;
}

.m-toast-success {
  /*background-size: 100% 100%;*/
  /*width: 220px;*/
  /*height: 255px;*/
  /*background: url("/static/images/success.svg") no-repeat;*/

  background: url("/static/images/toast_success.png");
  background-size: cover;
  width: 100px;
  height: 100px;
  overflow: hidden;
}
</style>
