import List from "./components/List.vue"
import Add from "./components/Add.vue"
import Detail from "./components/Detail.vue"
import Tax from "./components/Tax.vue"
import donationRoutes from "./donating/router"

export const BASE_URL = "/subsidy"

export default [
  { path: BASE_URL, component: List },
  { path: `${BASE_URL}/tax`, component: Tax },
  { path: `${BASE_URL}/add`, component: Add },
  { path: `${BASE_URL}/:id`, component: Detail },
  ...donationRoutes,
]