export interface Response {
    id: number 
    date: string

    height: number  | null
    weight: number  | null
    waist: number  | null
    bmi: number  | null

    systolic_bp: number  | null
    diastolic_bp: number  | null

    vision_right: number  | null
    vision_left: number  | null
    hearing_right: string | null
    hearing_left: string | null

    // 尿検査
    urinalysis: string | null

    // 血液検査（貧血・血球）
    rbc: number  | null
    hemoglobin: number  | null    // ヘモグロビン (g/dL)
    wbc: number  | null
    hematocrit: number  | null    // ヘマトクリット (%)
    platelets: number  | null     // 血小板数 (万/μL)
    esr: number  | null           // 赤沈 (mm/h)

    // 脂質
    hdl_cholesterol: number  | null  // HDL (mg/dL)
    ldl_cholesterol: number  | null  // LDL (mg/dL)
    triglycerides: number  | null    // 中性脂肪 (mg/dL)

    // 糖代謝
    blood_glucose: number  | null    // 血糖 (mg/dL)
    hba1c: number  | null            // HbA1c (%)

    // 肝機能
    ast: number  | null           // AST (U/L)
    alt: number  | null           // ALT (U/L)
    gamma_gtp: number  | null     // γ-GTP (U/L)

    // 心電図
    ecg: string | null                 // 心電図（所見）

    note: string | null                       // 備考

}


export type MetricKey = (
    'systolic_bp' | 
    'diastolic_bp' | 
    'bmi' | 
    'waist'|
    'hdl_cholesterol'|
    'ldl_cholesterol'|
    'triglycerides'|
    'blood_glucose'|
    'hba1c' |
    'ast' |
    'alt' |
    'gamma_gtp'
)

export interface Input {
    date: string

    height: number  | null
    weight: number  | null
    waist: number  | null

    systolic_bp: number  | null
    diastolic_bp: number  | null

    vision_right: number  | null
    vision_left: number  | null
    hearing_right: string | null
    hearing_left: string | null

    // 尿検査
    urinalysis: string | null

    // 血液検査（貧血・血球）
    rbc: number  | null
    hemoglobin: number  | null    // ヘモグロビン (g/dL)
    wbc: number  | null
    hematocrit: number  | null    // ヘマトクリット (%)
    platelets: number  | null     // 血小板数 (万/μL)
    esr: number  | null           // 赤沈 (mm/h)

    // 脂質
    hdl_cholesterol: number  | null  // HDL (mg/dL)
    ldl_cholesterol: number  | null  // LDL (mg/dL)
    triglycerides: number  | null    // 中性脂肪 (mg/dL)

    // 糖代謝
    blood_glucose: number  | null    // 血糖 (mg/dL)
    hba1c: number  | null            // HbA1c (%)

    // 肝機能
    ast: number  | null           // AST (U/L)
    alt: number  | null           // ALT (U/L)
    gamma_gtp: number  | null     // γ-GTP (U/L)

    // 心電図
    ecg: string | null                 // 心電図（所見）

    note: string | null                       // 備考
}


export interface Draft {
    date: Date | null

    height: number  | null
    weight: number  | null
    waist: number  | null

    systolic_bp: number  | null
    diastolic_bp: number  | null

    vision_right: number  | null
    vision_left: number  | null
    hearing_right: string | null
    hearing_left: string | null

    // 尿検査
    urinalysis: string | null

    // 血液検査（貧血・血球）
    rbc: number  | null
    hemoglobin: number  | null    // ヘモグロビン (g/dL)
    wbc: number  | null
    hematocrit: number  | null    // ヘマトクリット (%)
    platelets: number  | null     // 血小板数 (万/μL)
    esr: number  | null           // 赤沈 (mm/h)

    // 脂質
    hdl_cholesterol: number  | null  // HDL (mg/dL)
    ldl_cholesterol: number  | null  // LDL (mg/dL)
    triglycerides: number  | null    // 中性脂肪 (mg/dL)

    // 糖代謝
    blood_glucose: number  | null    // 血糖 (mg/dL)
    hba1c: number  | null            // HbA1c (%)

    // 肝機能
    ast: number  | null           // AST (U/L)
    alt: number  | null           // ALT (U/L)
    gamma_gtp: number  | null     // γ-GTP (U/L)

    // 心電図
    ecg: string | null                 // 心電図（所見）

    note: string | null                       // 備考
}
