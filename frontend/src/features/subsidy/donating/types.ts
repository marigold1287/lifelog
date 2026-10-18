export interface View {
    entry_id: number
    trade_date: string
    deduction_year: number
    shop: string
    is_shimin_zei_deduction: boolean
    is_kenmin_zei_deduction: boolean
    is_shotoku_zei_deduction: boolean
    total_shimin_zei_deduction: number
    total_kenmin_zei_deduction: number
    total_shotoku_zei_deduction: number
}

export interface Input {
    entry_id: number
    deduction_year: number
    is_shimin_zei_deduction: boolean
    is_kenmin_zei_deduction: boolean
    is_shotoku_zei_deduction: boolean
}


export interface Draft {
    entry_id: number | null
    deduction_year: number | null
    is_shimin_zei_deduction: boolean
    is_kenmin_zei_deduction: boolean
    is_shotoku_zei_deduction: boolean
}

export interface EntrySchema {
    id: number | null
    date: string
    shop: string
    label: string
}