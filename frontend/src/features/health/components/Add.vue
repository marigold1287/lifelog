<script setup lang="ts">
    import { ref, onMounted } from "vue"
    import type { Draft } from "../types"
    import { getErrorMessage } from "@/api"
    import { create } from "../api"
    import Form from "./Form.vue"
    import { useRouter } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()

    const health = ref<Draft>({
        date: new Date(),
        height: null,
        weight: null,
        waist: null,

        systolic_bp: null,
        diastolic_bp: null,

        vision_right: null,
        vision_left: null,
        hearing_right: null,
        hearing_left: null,

        // 尿検査
        urinalysis: null,

        // 血液検査（貧血・血球）
        rbc: null,
        hemoglobin: null,    // ヘモグロビン (g/dL)
        wbc: null,
        hematocrit: null,    // ヘマトクリット (%)
        platelets: null,     // 血小板数 (万/μL)
        esr: null,           // 赤沈 (mm/h)

        // 脂質
        hdl_cholesterol: null,  // HDL (mg/dL)
        ldl_cholesterol: null,  // LDL (mg/dL)
        triglycerides: null,    // 中性脂肪 (mg/dL)

        // 糖代謝
        blood_glucose: null,    // 血糖 (mg/dL)
        hba1c: null,            // HbA1c (%)

        // 肝機能
        ast: null,           // AST (U/L)
        alt: null,           // ALT (U/L)
        gamma_gtp: null,     // γ-GTP (U/L)

        // 心電図
        ecg: null,                 // 心電図（所見）

        note: null,                       // 備考
    })

    async function submit() {
        try {
            const record = await create(health.value)

            if (record?.id) {
                alert("登録が完了いたしました！")
                await router.push(`/health/${record.id}`)
            }
        } catch (error) {
            errorMessage.value = getErrorMessage(error)
        }
    }
</script>

<template>
    <Form 
        v-model="health"
        @submit="submit"
        :error-message="errorMessage"
    />

</template>