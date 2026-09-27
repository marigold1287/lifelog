<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import type { BillInput, BillApi } from "../types"
    import { getErrorMessage } from "@/api"
    import BillForm from "./Form.vue"
    import { useRouter } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()

    const props = defineProps<{
        api: BillApi
        baseUrl: string
        provider: string
    }>()

    const bill = ref<BillInput>({
        start_date: new Date(),
        end_date:  new Date(),
        usage: 0,
        total: 0,
        provider: props.provider,
    })

    const providers = ref<string[]>([])

    async function onSubmit() {
        try {
            const record = await props.api.create(bill.value);

            if (record && record.id) {
                alert("登録が完了いたしました！");
                await router.push(`${props.baseUrl}/${record.id}`);
            }
        } catch (error) {
            errorMessage.value = getErrorMessage(error)
        }
    }


    onMounted(async () => {
        providers.value = await props.api.getProviderList()
        const latest = await props.api.getLatest();
        if (latest) {
            const startDate = new Date(latest.end_date)
            startDate.setDate(startDate.getDate() + 1)

            bill.value.start_date = startDate
        }
    })
</script>

<template>
    <BillForm 
        v-model="bill"
        :providers="providers"
        @submit="onSubmit"
        :error-message="errorMessage"
    />

</template>