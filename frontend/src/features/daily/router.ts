import List from "./components/List.vue"
import Add from "./components/Add.vue"
import Detail from "./components/Detail.vue"

export default [
  { path: "/daily", component: List },
  { path: "/daily/add", component: Add },
  { path: "/daily/:id", component: Detail },
]