import List from "@/features/book/work/components/List.vue"
import Add from "@/features/book/work/components/Add.vue"
import Detail from "@/features/book/work/components/Detail.vue"

export default [
  { path: "/work", component: List },
  { path: "/work/add", component: Add },
  { path: "/work/:id", component: Detail },
]