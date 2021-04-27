import {createRouter, createWebHistory} from 'vue-router'
import Index from '../views/Index.vue'
import Problems from '../views/Problems.vue'
import ProblemDetail from "../views/ProblemDetail.vue";
import ContextDetail from "../views/ContextDetail.vue"
import Contexts from '../views/Contexts.vue'
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
    meta: {
      index: 1,
    },
    component: Index
  },
  {
    path: '/problems',
    name: 'Problems',
    meta: {
      index: 2,
    },
    component: Problems
  },
  {
    path: '/problems/:id',
    name: 'Problem',
    meta: {
      index: 3,
    },
    component: ProblemDetail
  },
  {
    path: '/contexts',
    name: 'Contexts',
    meta: {
      index: 4,
    },
    component: Contexts
  },
  {
    path: '/contexts/:id',
    name: 'Context',
    meta: {
      index: 5,
    },
    component: ContextDetail
  },
  {
    path: '/login',
    name: 'Login',
    meta: {
      index: 6,
    },
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    meta: {
      index: 7,
    },
    component: Register
  },
  {
    path: '/sregister',
    name: 'SRegister',
    meta: {
      index: 8,
    },
    component: SRegister
  },
  {
    path: '/account',
    name: 'Account',
    meta: {
      index: 9,
    },
    component: Account
  },
  {
    path: '/verify_email',
    name: 'VerifyEmail',
    meta: {
      index: 10,
    },
    component: VerifyEmail
  },
  {
    path: '/forget',
    name: 'Forget',
    meta: {
      index: 11,
    },
    component: Forget
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
