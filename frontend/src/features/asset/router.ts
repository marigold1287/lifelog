import List from "./components/List.vue"
import assetRoutes from "./account/router.ts"
import holdingRoutes from "./holding/router.ts"
import transactionRoutes from "./transaction/router.ts"
import kakeiboRoutes from "./kakeibo/router.ts"
export const BASE_URL = "/asset"

export default [
  { path: BASE_URL, component: List },
  ...assetRoutes,
  ...holdingRoutes,
  ...transactionRoutes,
  ...kakeiboRoutes,
]