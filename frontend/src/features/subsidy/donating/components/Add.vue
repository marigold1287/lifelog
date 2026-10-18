<script setup lang="ts">
    import { ref, onMounted } from "vue"
    import type { Draft } from "../types"
    import { getErrorMessage } from "@/api"
    import { create } from "../api"
    import Form from "./Form.vue"
    import { useRouter } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()

    const deduction = ref<Draft>({
        deduction_year: null,
        entry_id: null,
        is_shimin_zei_deduction: false,
        is_kenmin_zei_deduction: false,
        is_shotoku_zei_deduction: false,
    })

    async function submit() {
        try {
            const record = await create(deduction.value)

            if (record?.entry_id) {
                alert("登録が完了いたしました！")
                await router.push(`/subsidy/donation/${record.entry_id}`)
            }
        } catch (error) {
            errorMessage.value = getErrorMessage(error)
        }
    }
</script>

<template>
    <Form 
        v-model="deduction"
        @submit="submit"
        :error-message="errorMessage"
    />

</template>