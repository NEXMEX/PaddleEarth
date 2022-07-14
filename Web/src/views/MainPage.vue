<template>
   <el-container style="height:100%">
     <!-- 头部 -->
      <el-header>
        <common-header/>
      </el-header>

      <el-container>
        <transition
          appear
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInLeft"
        >
          <el-aside width="auto" >
            <common-left-aside/>
          </el-aside>
        </transition>

        <transition
          appear
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInRight"
        >
          <el-main><common-main style="padding:0;margin:0"/></el-main>
        </transition>
        <transition
          appear
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInRight"
          leave-active-class="animate__slideOutRight"
        >
          <el-aside width="50px"  class="RightAside"
            ><common-right-aside/>
          </el-aside>
        </transition>
      </el-container>
       <v-tour name="myTour" :steps="steps" :options="tourOptions"></v-tour>
    </el-container>
    
</template>

<script>
import CommonHeader from '../components/CommonHeader.vue'
import CommonLeftAside from'../components/CommonLeftAside.vue'
import CommonMain from'../components/CommonMain.vue'
import CommonRightAside from '../components/CommonRightAside.vue'
import steps from '../utils/steps.js'

export default {
    name:'MainPage',
    components:{
    CommonHeader,
    CommonLeftAside,
    CommonMain,
    CommonRightAside
},
    data(){
      return{
        isAnalysing:false,
        steps: steps,
         //引导页配置项
        tourOptions: {
          useKeyboardNavigation: false,
          labels: {
            buttonSkip: '跳过帮助',
            buttonPrevious: '上一步',
            buttonNext: '下一步',
            buttonStop: '我知道了'
          }
        },
        //背景图
        bg:require('../assets/background.png')
      } 
    },
    methods:{
      // 用户是否首次登录
    firstLogin() {
      const firstDate = localStorage.getItem('firstDate')
      // 获取当前时间（年月日）
      const now = new Date().toLocaleDateString()
      // 转换成时间戳
      const time = Date.parse(new Date(now))
      if (localStorage.getItem('firstDate')) {
        console.log('页面被刷新')
        this.guide()
        if (time > firstDate) {
          localStorage.setItem('firstDate', JSON.stringify(time))
        }
      } else {
        this.guide()
        localStorage.setItem('firstDate', JSON.stringify(time))
        console.log('首次被加载')
      }
    },
    // 页面引导
    guide() {
      console.log("im in guide")
      this.$tours['myTour'].start()
    }

    },


    mounted(){
      console.log(this.$tours)
      this.$bus.$on('showRightAside',(isAnalysing)=>{
            this.isAnalysing=isAnalysing
      })  
      this.$bus.$on('getLayers',(items)=>{
           console.log(items)
           this.isAnalysing=true
      })  
      this.$bus.$on('showHelper',(i)=>{
        i===1;
        this.$tours['myTour'].start()
      })
      this.firstLogin()
    },
    beforeDestroy(){
    try{
      document.body.style.background=`url(${this.bg}) no-repeat`;
    } catch(err){
      console.log(err.message,"err")
    }
    
  }
}
</script>

<style lang="less" scoped>

.el-header {
   background-color: #2c3740;
 
  color: rgb(242, 248, 246);
  
}

.el-aside {
  background-color: transparent;
  color: rgb(243, 236, 236);
  margin:10px; 
  font-family: "Hiragino Sans GB";
}

.el-main {
   
  color: rgb(252, 247, 247);
  font-family: "Hiragino Sans GB";
  height:650px;
  padding:0;
  margin: 10px;
   overflow-y: hidden ;
  border-radius: 3%; 
  border: 1px dashed;
}

</style>