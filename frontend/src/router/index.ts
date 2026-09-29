import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@/components/HomeView.vue"
import bookRoutes from "@/features/book/router"
import billRoutes from "@/features/bill/router"
import payslipRoutes from "@/features/payslip/router"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: "/", component: HomeView},
    ...bookRoutes,
    ...billRoutes,
    ...payslipRoutes,
  ],
})

export default router
