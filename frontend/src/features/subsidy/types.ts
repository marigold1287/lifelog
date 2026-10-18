export interface View {
    id: number
    year: number
    amount_after_salary_deductions: number
    shotoku_zei_basic_deduction: number
    jumin_zei_basic_deduction: number
    shotoku_zei_fixed_deduction: number
    jumin_zei_fixed_deduction: number
}

export interface Input {
    year: number
    amount_after_salary_deductions: number
    shotoku_zei_basic_deduction: number
    jumin_zei_basic_deduction: number
    shotoku_zei_fixed_deduction: number
    jumin_zei_fixed_deduction: number
}

export interface Tax {
    nenmatsu_chosei: NenmatsuChosei[]
    kakutei_shinkoku: KakuteiShinkoku[]
    jumin_zei: JuminZei[]
}


export interface NenmatsuChosei {
    year: number
    nenshu: number
    shiharai_kingaku: number
    ideco: number
    shakai_hoken_deduction: number
    total_shakai_hoken_deduction: number
    seimei_hoken_deduction: number
    basic_deduction: number
    total_deduction: number
    kazei_shotoku: number
    paid_shotoku_zei: number
    shotoku_zei: number
    nenmatsu_chosei_kabusoku: number
}

export interface KakuteiShinkoku {
    year: number
    shotoku: number
    zatsu_shotoku: number
    haitou: number
    kazei_shotoku: number
    furusato: number
    shotoku_zei_donation: number
    shotoku_donation_deduction: number
    shotoku_deduction: number
    zeigaku_deduction: number
    shotoku_zei: number
    paid_shotoku_zei: number
    kanpu: number
}


export interface JuminZei {
    year: number
    shotoku: number
    total_deduction: number
    kazei_shotoku: number
    shimin_zei: number
    kenmin_zei: number
    jumin_zei: number
    furusato_limit: number
}