<template>
<footer class="login-footer">
  <ul>
    <li>关于我们</li>
    <li>法律声明</li>
    <li>服务条款</li>
    <li>联系方式</li>
  </ul>
  <p>地址：浙江省杭州市萧山区宝盛世纪中心 邮编：xxxxx </p>
  <p>建议使用谷歌浏览器</p>
</footer>
</template>
<script type="text/ecmascript-6">
    export default {
        data() {
            return {}
        },
        methods: {},
        created() {

        }
    }
</script>
<style lang="less" rel="stylesheet/less" scoped>
  .login-footer{
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    text-align: center;
    height: auto;
    background-color: #fff;
    font-size: 0.12rem;
    line-height: 0.20rem;
    color: #999999;
    padding: 0.1rem 0;
    ul{
      li{
        display: inline-block;
        padding: 0 0.1rem;
        color: #000;
      }
    }
  }
</style>
