<script setup lang="ts">
    import { ref, computed } from "vue"
    import type { Input } from "../types"
    import { payslipFields } from "../types"
    import CompactInputForm from "@/components/CompactInputForm.vue";

    const payslip = defineModel<Input>({ required: true })

    const props = withDefaults(defineProps<{
        submitButtonLabel?: string
        errorMessage?: string
    }>(), {
        submitButtonLabel: "Submit",
        errorMessage: "",
    })

    const payments = computed(() => {
        return (Object.keys(payslipFields) as Array<keyof typeof payslipFields>).filter(
            (key) => payslipFields[key].type === "支給"
        )
    })

    const totalPayment = computed(() => {
        return payments.value.reduce((sum, key) => {
            const value = Number(payslip.value[key]) || 0
            return sum + value
        }, 0)
    })

    const deductions = computed(() => {
        return (Object.keys(payslipFields) as Array<keyof typeof payslipFields>).filter(
            (key) => payslipFields[key].type === "控除"
        )
    })

    const totalDeduction = computed(() => {
        return deductions.value.reduce((sum, key) => {
            const value = Number(payslip.value[key]) || 0
            return sum + value
        }, 0)
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
        <h2>支給日</h2>
        <v-date-input
            v-model="payslip.date"
            density="compact"
            hide-details
        />

        <h2>支給</h2>
        <CompactInputForm
            v-for="key in payments"
            :key="key"
            v-model="payslip[key]"
            :label="payslipFields[key].label"
        />

        <p>総支給額: {{ totalPayment }}</p>

        <h2>控除</h2>
        <CompactInputForm
            v-for="key in deductions"
            :key="key"
            v-model="payslip[key]"
            :label="payslipFields[key].label"
        />

        <p>控除合計: {{ totalDeduction }}</p>

        <p>支給額: {{ totalPayment - totalDeduction }}</p>

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