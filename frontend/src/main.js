import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import CreateNote from './components/CreateNote.vue'
import ViewNote from './components/ViewNote.vue'

const routes = [
  { path: '/', component: CreateNote },
  { path: '/note/:id', component: ViewNote }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
