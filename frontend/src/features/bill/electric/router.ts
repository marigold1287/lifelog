import List from "./components/List.vue"
import Add from "./components/Add.vue"
import Detail from "./components/Detail.vue"

export const BASE_URL = "/bill/electric"

export default [
  { path: BASE_URL, component: List },
  { path: `${BASE_URL}/add`, component: Add },
  { path: `${BASE_URL}/:id`, component: Detail },
]