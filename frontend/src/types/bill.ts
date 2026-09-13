export interface BillRecord {
  id: number | null
  start_date: string
  end_date: string
  usage: number
  total: number
  provider: string
}
