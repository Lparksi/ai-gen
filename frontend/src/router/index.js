import { createRouter, createWebHistory } from 'vue-router'
import DiaryList from '../views/DiaryList.vue'
import DiaryDetail from '../views/DiaryDetail.vue'
import DiaryEdit from '../views/DiaryEdit.vue'

const routes = [
  {
    path: '/',
    name: 'DiaryList',
    component: DiaryList
  },
  {
    path: '/diary/:id',
    name: 'DiaryDetail',
    component: DiaryDetail,
    props: true
  },
  {
    path: '/edit/:id?',
    name: 'DiaryEdit',
    component: DiaryEdit,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
