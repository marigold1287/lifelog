import List from "@/features/book/author/components/List.vue"
import Add from "@/features/book/author/components/Add.vue"
import Detail from "@/features/book/author/components/Detail.vue"

export default [
  { path: "/author", component: List },
  { path: "/author/add", component: Add },
  { path: "/author/:id", component: Detail },
]