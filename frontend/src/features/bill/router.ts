import ElectricRoutes from "@/features/bill/electric/router"
import WaterRoutes from "@/features/bill/water/router"
import GasRoutes from "@/features/bill/gas/router"

export default [
    ...ElectricRoutes,
    ...WaterRoutes,
    ...GasRoutes,
]