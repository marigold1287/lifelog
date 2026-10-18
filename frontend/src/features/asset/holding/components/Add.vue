<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import type { Input } from "../types.ts"
    import { create } from "../api.ts"
    import { getErrorMessage } from "@/api"
    import Form from "./Form.vue"
    import { useRouter } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()

    const holding = ref<Input>({
        name: "",
        type: "cash",
        symbol: null,
        currency: "JPY",
        price_source: null,
        price_per_units: 1
    })

    async function onSubmit() {
        try {
            const record = await create(holding.value);

            if (record && record.id) {
                alert("登録が完了いたしました！");
                await router.push(`/holding/${record.id}`);
            }
        } catch (error) {
            errorMessage.value = getErrorMessage(error)
        }
    }
</script>

<template>
    <Form 
        v-model="holding"
        @submit="onSubmit"
        :error-message="errorMessage"
    />

</template>