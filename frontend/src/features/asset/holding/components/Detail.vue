<script setup lang="ts">
    import { onMounted, ref, watch, computed } from "vue"
    import { useRoute, useRouter } from "vue-router"
    import { get, update, remove, getPrices } from "../api.ts"
    import { BASE_URL } from "../router.ts"
    import type { Input, Response, PriceInput } from "../types.ts"
    import { CustomApiError, getErrorMessage } from "@/api"
    import { formatMoney } from "@/utils/utils"
    import Form from "./Form.vue"
    import Chart from "./Chart.vue"

    const holding = ref<Input | null>(null)
    const response = ref<Response>()
    const prices = ref<PriceInput[]>([])
    const entries = computed(() => response.value?.entries ?? [])

    const route = useRoute()
    const router = useRouter()
    const errorMessage = ref("")

    const headers = [
        { title: '', key: 'account' },
        { title: '総量', key: 'total_quantity' },
        { title: '取得コスト', key: 'acquisition_cost' },
        { title: '現在価値', key: 'current_value' },
        { title: '損益', key: 'profit_loss' },
        { title: '損益割合, %', key: 'profit_loss_rate' },
    ]

    async function onSubmitUpdate() {
        if (!holding.value) return;

        try {
            await update(holding.value, `${route.params.id}`);
            alert("更新しました")
        } catch (error) {
            errorMessage.value = getErrorMessage(error);
        }
    }

    async function onSubmitDelete() {
        if (!holding.value) return;
        if (!confirm("削除しますか?")) return;

        try {
            await remove(`${route.params.id}`)
            alert("削除しました");
            
            await router.push(BASE_URL);
        } catch (error) {
            if (error instanceof CustomApiError) {
                errorMessage.value = error.message;
            }
        }
    }

    onMounted(async () => {
        const res = await get(`${route.params.id}`);
        response.value = res;
        prices.value = await getPrices(`${route.params.id}`);
        
        if (res) {
            const { entries, ...formData } = res;
            holding.value = formData;
            console.log(entries)
        }
    })
</script>

<template>
    <div v-if="holding">
        <Form 
            v-model="holding"
            :error-message="errorMessage"
            @submit="onSubmitUpdate"
        />
        <v-btn
            class="mt-6"
            color="error"
            prepend-icon="mdi-delete"
            variant="flat"
            type="button"
            @click="onSubmitDelete"
        >
        Delete
        </v-btn>

        <v-data-table
            :items="entries"
            :headers="headers"
        >
            <template #item.average_unit_price="{ value }">{{ formatMoney(value) }}</template>
            <template #item.acquisition_cost="{ value }">{{ formatMoney(value) }}</template>
            <template #item.current_value="{ value }">{{ formatMoney(value) }}</template>
            <template #item.profit_loss="{ value }">{{ formatMoney(value) }}</template>
            <template #item.profit_loss_rate="{ value }">{{ value?.toLocaleString() }}</template>
        </v-data-table>
    </div>

    <Chart
        :data="prices"
    ></Chart>

</template>