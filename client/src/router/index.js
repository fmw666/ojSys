import {createRouter, createWebHistory} from 'vue-router'
import Index from '../views/Index.vue'
import Problems from '../views/Problems.vue'
import ProblemPage from "../views/ProblemPage.vue";
import Context from '../views/Context.vue'
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"
import SRegister from "../views/SRegister.vue";
import Account from "../views/Account.vue"
import VerifyEmail from "../views/VerifyEmail.vue"
import Forget from "../views/Forget.vue"


const routes = [
  {
    path: '/',
    name: 'Index',
    component: Index
  },
  {
    path: '/problems',
    name: 'Problems',
    component: Problems
  },
  {
    path: '/problems/:id',
    name: 'Problem',
    component: ProblemPage
  },
  {
    path: '/context',
    name: 'Context',
    component: Context
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/sregister',
    name: 'SRegister',
    component: SRegister
  },
  {
    path: '/account',
    name: 'Account',
    component: Account
  },
  {
    path: '/verify_email',
    name: 'VerifyEmail',
    component: VerifyEmail
  },
  {
    path: '/forget',
    name: 'Forget',
    component: Forget
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
