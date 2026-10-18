<script setup lang="ts">
    import { onMounted, ref, watch, computed } from "vue"
    import { useRoute, useRouter } from "vue-router"
    import { get, update, remove } from "../api.ts"
    import { BASE_URL } from "../router.ts"
    import type { Input, Response } from "../types.ts"
    import { CustomApiError, getErrorMessage } from "@/api"
    import Form from "./Form.vue"

    const holding = ref<Input | null>(null)
    const response = ref<Response>()
    const entries = computed(() => response.value?.entries ?? [])

    const total = computed(() => {
        const quantity = entries.value.reduce(
            (sum, item) => sum + item.total_quantity,
            0
        )

        const acquisitionCost = entries.value.reduce(
            (sum, item) => sum + item.acquisition_cost,
            0
        )

        const currentValue = entries.value.reduce(
            (sum, item) => sum + item.current_value,
            0
        )

        const pricePerUnits = response.value?.price_per_units ? response.value?.price_per_units : 1

        const averageUnitPrice = quantity > 0 ? acquisitionCost / quantity * pricePerUnits : 0

        const profitLoss = currentValue - acquisitionCost

        console.log({
            total_quantity: quantity,
            average_unit_price: averageUnitPrice,
            acquisition_cost: acquisitionCost,
            current_value: currentValue,
            profit_loss: profitLoss,
            profit_loss_rate: acquisitionCost
            ? profitLoss / acquisitionCost * 100
            : 0,
        })

        return {
            total_quantity: quantity,
            average_unit_price: averageUnitPrice,
            acquisition_cost: acquisitionCost,
            current_value: currentValue,
            profit_loss: profitLoss,
            profit_loss_rate: acquisitionCost
            ? profitLoss / acquisitionCost * 100
            : 0,
        }
    })

    
    const route = useRoute()
    const router = useRouter()
    const errorMessage = ref("")

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
        >
            <template #body.append>
                <tr class="font-weight-bold">
                    <td>合計</td>
                    <td>
                    {{ total.total_quantity.toLocaleString() }}
                    </td>
                    <td>{{ total.average_unit_price.toLocaleString() }}</td>
                    <td>
                    {{ total.acquisition_cost.toLocaleString() }}
                    </td>
                    <td>―</td>
                    <td>
                    {{ total.current_value.toLocaleString() }}
                    </td>
                    <td>
                    {{ total.profit_loss.toLocaleString() }}
                    </td>
                    <td>
                    {{ total.profit_loss_rate.toFixed(2) }}%
                    </td>
                </tr>
            </template>
        </v-data-table>
    </div>

</template>