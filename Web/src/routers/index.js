import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)
const routes=[
    {
        path:'/welcome',
        name:'Welcome',
        component:()=>import('../views/WelcomePage.vue')
    },
    {
        path:'/login',
        name:'Login',
        component:()=>import('../views/LoginPage.vue')
    },
    {
        path:'/home',
        name:'home',
        component:()=>import('../views/MainPage.vue')
    },
    {
        path:'/register',
        name:'register',
        component:()=>import('../views/RegisterPage.vue')
    }

]
export default new VueRouter({
    //mode:'history',
    base: '/demo/',
    routes,
})