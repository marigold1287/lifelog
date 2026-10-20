<script setup lang="ts">
    import { ref, onMounted } from "vue"
    import type { Draft } from "../types"
    import { getErrorMessage } from "@/api"
    import { create } from "../api"
    import Form from "./Form.vue"
    import { useRouter } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()

    const daily = ref<Draft>({
        date: new Date(),
        weight: null,
        room_temperature:null,
        room_humidity: null,
        body_temperature: null
    })

    async function submit() {
        try {
            const record = await create(daily.value)

            if (record?.id) {
                alert("登録が完了いたしました！")
                await router.push(`/daily/${record.id}`)
            }
        } catch (error) {
            errorMessage.value = getErrorMessage(error)
        }
    }
</script>

<template>
    <Form 
        v-model="daily"
        @submit="submit"
        :error-message="errorMessage"
    />

</template>