import List from "@/features/book/publisher/components/List.vue"
import Add from "@/features/book/publisher/components/Add.vue"
import Detail from "@/features/book/publisher/components/Detail.vue"

export default [
  { path: "/publisher", component: List },
  { path: "/publisher/add", component: Add },
  { path: "/publisher/:id", component: Detail },
]