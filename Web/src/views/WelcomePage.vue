<template>
<div class="welcome" ref="welcome">
    <div class="welcome-box">
         <transition
          appear
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInLeft"
           leave-active-class="animate__slideOutLeft"
        >
       <div class="message"></div>      
        </transition>
             <transition
          appear
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInRight"
            leave-active-class="animate__slideOutRight"
        >
           <el-button @click="toMainPage" class="btn-container">
            立即体验
            </el-button>    
        </transition>


    </div>
    
</div>  
</template>

<script>
export default {
    name:'WelcomePage',
    methods:{
        toMainPage(){
            this.$router.push('/home');
            
        }
    }
}
</script>

<style>
html,
body{
    /* display:flex;
    flex:vertical;
    align-items: center; */
    background: url('../assets/background.png') no-repeat;
    height: 100vh;
    width:100%;
    background-size: 100% 100%;
}
.welcome-box{
    margin-top:275px;
    margin-left:250px;
}
.message{
    background: url('../assets/welcome-message.png') no-repeat;
     background-size: 624px 175px;
     height: 175px;
    width:624px;
   

    z-index: 10000;
}
.btn-container{
    background-color: #7CECD7;
    
    border:none;
    height: 70px;
    width: 150px;
    font-size: large;

}
</style>