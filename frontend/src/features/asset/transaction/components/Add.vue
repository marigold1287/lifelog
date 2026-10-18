<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import type { TransactionInput, TransactionDraft } from "../types.ts"
    import { create } from "../api.ts"
    import { getErrorMessage } from "@/api"
    import Form from "./Form.vue"
    import { useRouter } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()

    const transaction = ref<TransactionDraft>({
        trade_date: new Date(),
        type: "expense",
        shop: null,
        note: null,
        entries: [{
            id: null,
            account_id: null,
            holding_id: null,
            quantity: null,
            unit_price: null,
            item_name: null,
            memo: null,
        }]
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
</script>

<template>
    <Form 
        v-model="transaction"
        @submit="onSubmit"
        :error-message="errorMessage"
    />

</template>