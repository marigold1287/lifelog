import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@/components/HomeView.vue"
import bookRoutes from "@/features/book/router"
import billRoutes from "@/features/bill/router"
import payslipRoutes from "@/features/payslip/router"
import assetRoutes from "@/features/asset/router"
import subsidyRoutes from "@/features/subsidy/router"
import dailyRoutes from "@/features/daily/router"
import healthRoutes from "@/features/health/router"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: "/", component: HomeView},
    ...bookRoutes,
    ...billRoutes,
    ...payslipRoutes,
    ...assetRoutes,
    ...subsidyRoutes,
    ...dailyRoutes,
    ...healthRoutes,
  ],
})

export default router
