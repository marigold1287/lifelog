import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@/components/HomeView.vue"
import publisherRoutes from "@/features/book/publisher/router"
import authorRoutes from "@/features/book/author/router"
import workRoutes from "@/features/book/work/router"
import bookRoutes from "@/features/book/book/router"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: "/", component: HomeView},
    ...publisherRoutes,
    ...authorRoutes,
    ...workRoutes,
    ...bookRoutes,
  ],
})

export default router
