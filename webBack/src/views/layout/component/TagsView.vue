<template>
  <div class="tags-view-container">
    <!--<scroll-pane class='tags-view-wrapper' ref='scrollPane'>-->
      <!--<router-link ref='tag' class="tags-view-item" :class="isActive(tag)?'active':''" v-for="tag in Array.from(visitedViews)"-->
        <!--:to="tag" :key="tag.path" @contextmenu.prevent.native="openMenu(tag,$event)">-->
        <!--{{generateTitle(tag.title)}}-->
        <!--<span class='el-icon-close' @click.prevent.stop='closeSelectedTag(tag)'></span>-->
      <!--</router-link>-->
    <!--</scroll-pane>-->
    <!--<ul class='contextmenu' v-show="visible" :style="{left:left+'px',top:top+'px'}">-->
      <!--<li @click="closeSelectedTag(selectedTag)">{{$t('tagsView.close')}}</li>-->
      <!--<li @click="closeOthersTags">{{$t('tagsView.closeOthers')}}</li>-->
      <!--<li @click="closeAllTags">{{$t('tagsView.closeAll')}}</li>-->
    <!--</ul>-->
  </div>
</template>

<script>
// import ScrollPane from '@/component/ScrollPane'
// import { generateTitle } from '@/utils/i18n'

export default {
  // component: { ScrollPane },
  data() {
    return {
      visible: false,
      top: 0,
      left: 0,
      selectedTag: {}
    }
  },
  computed: {

  },
  watch: {

  },
  mounted() {

  },
  methods: {

  }
}
</script>

<style rel="stylesheet/less" lang="less" scoped>
</style>

