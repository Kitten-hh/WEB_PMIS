<template>
    <BlankPageLayout>
        <template v-slot:page-Details>
          <textarea id="mySavedModel" style="width:100%;height:300px">
          { "class": "go.GraphLinksModel",
          "linkFromPortIdProperty": "fromPort",
          "linkToPortIdProperty": "toPort",
          "nodeDataArray": [

            ],
          "linkDataArray": [

            ]}
            
          </textarea>          
        </template>
    </BlankPageLayout>
</template>

<script>
import BlankPageLayout from '@components/looper/layout/page/BlankPageLayout.vue'
export default {
  name: 'DialyPage',
  data() {
  },
  components:{
      BlankPageLayout
  },
}
</script>

<style scoped>
  >>> .page-title-bar {
    display:none;
  }
  >>> .page-inner {
    padding:0px;
  }
</style>