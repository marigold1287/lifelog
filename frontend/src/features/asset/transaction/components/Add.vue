<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import type { TransactionInput, TransactionDraft } from "../types.ts"
    import { create } from "../api.ts"
    import { getErrorMessage } from "@/api"
    import { get } from "../api.ts"
    import Form from "./Form.vue"
    import { useRouter, useRoute } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()
    const route = useRoute()

    const transaction = ref<TransactionDraft>({
        trade_date: new Date(),
        type: 'expense',
        shop: null,
        note: null,
        entries: []
    })

    async function onSubmit() {
        try {
            const record = await create(transaction.value);

            if (record && record.id) {
                alert("登録が完了いたしました！");
                await router.push(`/transaction/${record.id}`);
            }
        } catch (error) {
            errorMessage.value = getErrorMessage(error)
        }
    }

    onMounted(async () => {
        const transactionId = route.query.transaction_id;

        if (transactionId && !isNaN(Number(transactionId))) {
            const copySource = await get(Number(transactionId))
            if (copySource !== null) {
                transaction.value = {
                    ...copySource,
                    trade_date: new Date()
                }
            }
        } 
    })
</script>

<template>
    <h1>登録フォーム</h1>
    <Form 
        v-model="transaction"
        @submit="onSubmit"
        :error-message="errorMessage"
    />

</template>