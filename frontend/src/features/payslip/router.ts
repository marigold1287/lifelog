import List from "./components/List.vue"
import Add from "./components/Add.vue"
import Detail from "./components/Detail.vue"

export default [
  { path: "/payslip", component: List },
  { path: "/payslip/add", component: Add },
  { path: "/payslip/:id", component: Detail },
]