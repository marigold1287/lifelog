<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import type { Input } from "../types.ts"
    import { create } from "../api.ts"
    import { getErrorMessage } from "@/api"
    import Form from "./Form.vue"
    import { useRouter } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()

    const account = ref<Input>({
        name: "",
        type: "cash",
        currency: "JPY",
        parent_id: null,
        sort_order: 0
    })

    async function onSubmit() {
        try {
            const record = await create(account.value);

            if (record && record.id) {
                alert("登録が完了いたしました！");
                await router.push(`/account/${record.id}`);
            }
        } catch (error) {
            errorMessage.value = getErrorMessage(error)
        }
    }
</script>

<template>
    <Form 
        v-model="account"
        @submit="onSubmit"
        :error-message="errorMessage"
    />

</template>