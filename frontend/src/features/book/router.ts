import publisherRoutes from "@/features/book/publisher/router"
import authorRoutes from "@/features/book/author/router"
import workRoutes from "@/features/book/work/router"
import bookRoutes from "@/features/book/book/router"

export default [
    ...publisherRoutes,
    ...authorRoutes,
    ...workRoutes,
    ...bookRoutes,
]