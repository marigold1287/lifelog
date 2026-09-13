import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@/components/HomeView.vue"
import bookRoutes from "@/features/book/router"
import billRoutes from "@/features/bill/router"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: "/", component: HomeView},
    ...bookRoutes,
    ...billRoutes,
  ],
})

export default router
