import List from "./components/List.vue"
import Add from "./components/Add.vue"
import Detail from "./components/Detail.vue"

export default [
  { path: "/health", component: List },
  { path: "/health/add", component: Add },
  { path: "/health/:id", component: Detail },
]