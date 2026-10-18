<script setup lang="ts">
    import { ref, onMounted } from "vue"
    import type { Input } from "../types"
    import { getErrorMessage } from "@/api"
    import { create } from "../api"
    import Form from "./Form.vue"
    import { useRouter } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()

    const currentYear = new Date().getFullYear();

    const subsidy = ref<Input>({
        year: currentYear,
        amount_after_salary_deductions: 0,
        shotoku_zei_basic_deduction: 0,
        jumin_zei_basic_deduction: 0,
        shotoku_zei_fixed_deduction: 0,
        jumin_zei_fixed_deduction: 0,
    })

    async function submit() {
        try {
            const record = await create(subsidy.value)

            if (record?.id) {
                alert("登録が完了いたしました！")
                await router.push(`/subsidy/${record.id}`)
            }
        } catch (error) {
            errorMessage.value = getErrorMessage(error)
        }
    }
</script>

<template>
    <Form 
        v-model="subsidy"
        @submit="submit"
        :error-message="errorMessage"
    />

</template>