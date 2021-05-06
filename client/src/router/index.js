import {createRouter, createWebHistory} from 'vue-router'
import Index from '../views/Index.vue'
import Problems from '../views/Problems.vue'
import ProblemDetail from "../views/ProblemDetail.vue";
import ContestDetail from "../views/ContestDetail.vue"
import Contests from '../views/Contests.vue'
import Forum from '../views/Forum.vue'
import ForumDetail from '../views/ForumDetail.vue'
import ForumPost from "../views/ForumPost.vue"
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
    path: '/contests',
    name: 'Contests',
    meta: {
      index: 4,
    },
    component: Contests
  },
  {
    path: '/contests/:id',
    name: 'Contest',
    meta: {
      index: 5,
    },
    component: ContestDetail
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
  },
  {
    path: '/forum',
    name: 'Forum',
    meta: {
      index: 12,
    },
    component: Forum
  },
  {
    path: '/forum/:id',
    name: 'ForumDetail',
    meta: {
      index: 13,
    },
    component: ForumDetail
  },
  {
    path: '/forum_post',
    name: 'ForumPost',
    meta: {
      index: 14,
    },
    component: ForumPost
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
