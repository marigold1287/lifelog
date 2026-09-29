export interface View {
  id: number
  date: string
  total_shikyu: number
  total_kojo: number
  tedori: number
}

export interface Input {
    date: Date
    honkyu: number
    noryokukyu: number
    mibunkyu: number
    shokuji_teate: number
    kenkyuin_teate: number
    tsukin_teate: number
    jutaku_teate: number
    nitto_teate: number
    kekkin_koujo: number
    jitan_kyushutsu_teate: number
    shoyo: number
    shoyo_kakyu: number
    tokubetsu_kakyu: number
    tokushu_kinmu_teate: number
    sonota_shikyu: number

    kenko_hoken: number
    kosei_nenkin: number
    koyo_hoken: number
    kodomo_shienkin: number
    shotoku_zei: number
    jumin_zei: number
    senyukaihi: number
    shokuji_dai: number
    shataku_ryo: number
    ryohi: number
    seimei_hoken: number
    sonota_kojo: number
    nencho_kabusoku: number
}

export type Response = Omit<Input, 'date'> & {
    date: string
}

export const payslipFields: Record<
    Exclude<keyof Input, "date">,
    {
        label: string
        type: "支給" | "控除"
    }
> = {
    honkyu: {
        label: "本給",
        type: "支給",
    },
    noryokukyu: {
        label: "能力給",
        type: "支給",
    },
    mibunkyu: {
        label: "身分給",
        type: "支給",
    },
    shokuji_teate: {
        label: "食事手当",
        type: "支給",
    },
    kenkyuin_teate: {
        label: "研究員手当",
        type: "支給",
    },
    tsukin_teate: {
        label: "通勤手当",
        type: "支給",
    },
    jutaku_teate: {
        label: "住宅手当",
        type: "支給",
    },
    nitto_teate: {
        label: "日当手当",
        type: "支給",
    },
    kekkin_koujo: {
        label: "欠勤控除",
        type: "支給",
    },
    jitan_kyushutsu_teate: {
        label: "時短休出手当",
        type: "支給",
    },
    shoyo: {
        label: "賞与",
        type: "支給",
    },
    shoyo_kakyu: {
        label: "賞与加給",
        type: "支給",
    },
    tokubetsu_kakyu: {
        label: "特別加給",
        type: "支給",
    },
    tokushu_kinmu_teate: {
        label: "特殊勤務手当",
        type: "支給",
    },
    sonota_shikyu: {
        label: "その他支給",
        type: "支給",
    },

    kenko_hoken: {
        label: "健康保険",
        type: "控除",
    },
    kosei_nenkin: {
        label: "厚生年金",
        type: "控除",
    },
    koyo_hoken: {
        label: "雇用保険",
        type: "控除",
    },
    kodomo_shienkin: {
        label: "子ども支援金",
        type: "控除",
    },
    shotoku_zei: {
        label: "所得税",
        type: "控除",
    },
    jumin_zei: {
        label: "住民税",
        type: "控除",
    },
    senyukaihi: {
        label: "千友会費",
        type: "控除",
    },
    shokuji_dai: {
        label: "食事代",
        type: "控除",
    },
    shataku_ryo: {
        label: "社宅料",
        type: "控除",
    },
    ryohi: {
        label: "寮費",
        type: "控除",
    },
    seimei_hoken: {
        label: "生命保険",
        type: "控除",
    },
    sonota_kojo: {
        label: "その他控除",
        type: "控除",
    },
    nencho_kabusoku: {
        label: "年調過不足",
        type: "控除",
    },
} 