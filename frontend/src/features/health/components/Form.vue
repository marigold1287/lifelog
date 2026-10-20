<script setup lang="ts">
    import { ref, computed } from "vue"
    import type { Draft } from "../types"
    import CompactInputForm from "@/components/CompactInputForm.vue";

    const health = defineModel<Draft>({ required: true })

    const props = withDefaults(defineProps<{
        submitButtonLabel?: string
        errorMessage?: string
    }>(), {
        submitButtonLabel: "Submit",
        errorMessage: "",
    })

    const emit = defineEmits<{
        submit: []
    }>()
    const form = ref()

    async function onSubmit() {
        const { valid } = await form.value.validate()

        if (!valid) {
            return
        }

        emit("submit")
    }

</script>

<template>
    <v-form @submit.prevent="onSubmit" ref="form">
        <h2>日付</h2>
        <v-date-input
            v-model="health.date"
            density="compact"
            hide-details
        />

        <h1>身体測定</h1>
        <h2>身長, cm</h2>
        <v-number-input
            v-model="health.height"
            :step="0.1"
            :precision="2"
            hide-details
            density="compact"
        />
        <h2>体重, kg</h2>
        <v-number-input
            v-model="health.weight"
            :step="0.1"
            :precision="2"
            hide-details
            density="compact"
        />
        <h2>腹囲, cm</h2>
        <v-number-input
            v-model="health.waist"
            :step="0.1"
            :precision="2"
            hide-details
            density="compact"
        />

        <h1>血圧</h1>
        <h2>最高血圧</h2>
        <v-number-input
            v-model="health.systolic_bp"
            hide-details
            density="compact"
        />
        <h2>最低血圧</h2>
        <v-number-input
            v-model="health.diastolic_bp"
            hide-details
            density="compact"
        />

        <h1>視力・聴力</h1>
        <h2>右視力</h2>
        <v-number-input
            v-model="health.vision_right"
            :step="0.1"
            :precision="1"
            hide-details
            density="compact"
        />
        <h2>左視力</h2>
        <v-number-input
            v-model="health.vision_left"
            :step="0.1"
            :precision="1"
            hide-details
            density="compact"
        />
        <h2>右聴力(Aなど)</h2>
        <v-text-field
            v-model="health.hearing_right"
            hide-details
            density="compact"
        />
        <h2>左聴力</h2>
        <v-text-field
            v-model="health.hearing_left"
            hide-details
            density="compact"
        />

        <h1>血液検査</h1>
        <h2>赤血球数 (万/μL)</h2>
        <v-number-input
            v-model="health.rbc"
            hide-details
            density="compact"
        />
        <h2>ヘモグロビン (g/dL)</h2>
        <v-number-input
            v-model="health.hemoglobin"
            :step="0.1"
            :precision="1"
            hide-details
            density="compact"
        />
        <h2>白血球数 (/μL)</h2>
        <v-number-input
            v-model="health.wbc"
            hide-details
            density="compact"
        />
        <h2>ヘマトクリット (%)</h2>
        <v-number-input
            v-model="health.hematocrit"
            :step="0.1"
            :precision="1"
            hide-details
            density="compact"
        />
        <h2>血小板数 (万/μL)</h2>
        <v-number-input
            v-model="health.platelets"
            :step="0.1"
            :precision="1"
            hide-details
            density="compact"
        />
        <h2>赤沈 (mm/h)</h2>
        <v-number-input
            v-model="health.esr"
            :step="0.1"
            :precision="1"
            hide-details
            density="compact"
        />

        <h1>脂質</h1>
        <h2>HDL (mg/dL)</h2>
        <v-number-input
            v-model="health.hdl_cholesterol"
            :step="0.1"
            :precision="1"
            hide-details
            density="compact"
        />
        <h2>LDL (mg/dL)</h2>
        <v-number-input
            v-model="health.ldl_cholesterol"
            :step="0.1"
            :precision="1"
            hide-details
            density="compact"
        />
        <h2>中性脂肪 (mg/dL)</h2>
        <v-number-input
            v-model="health.triglycerides"
            :step="0.1"
            :precision="1"
            hide-details
            density="compact"
        />

        <h1>糖代謝</h1>
        <h2>血糖 (mg/dL)</h2>
        <v-number-input
            v-model="health.blood_glucose"
            :step="0.1"
            :precision="1"
            hide-details
            density="compact"
        />
        <h2>HbA1c (%)</h2>
        <v-number-input
            v-model="health.hba1c"
            :step="0.1"
            :precision="1"
            hide-details
            density="compact"
        />

        <h1>肝機能</h1>
        <h2>AST (U/L)</h2>
        <v-number-input
            v-model="health.ast"
            :step="0.1"
            :precision="1"
            hide-details
            density="compact"
        />
        <h2>ALT (U/L)</h2>
        <v-number-input
            v-model="health.alt"
            :step="0.1"
            :precision="1"
            hide-details
            density="compact"
        />
        <h2>γ-GTP (U/L)</h2>
        <v-number-input
            v-model="health.gamma_gtp"
            :step="0.1"
            :precision="1"
            hide-details
            density="compact"
        />

        <h1>心電図</h1>
        <v-text-field
            v-model="health.ecg"
            hide-details
            density="compact"
        />

        <h1>その他</h1>
        <v-textarea
            v-model="health.note"
            hide-details
            density="compact"
        />

        <v-btn
        class="mt-6"
        prepend-icon="mdi-send"
        variant="outlined"
        type="submit"
        >
        {{ submitButtonLabel }}
        </v-btn>
        <p v-if="errorMessage" class="error-message" style="color: red;">
            {{ errorMessage }}
        </p>

    </v-form>


</template>