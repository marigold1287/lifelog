<script setup lang="ts">
    import { onMounted, ref, watch, computed } from "vue"
    import { useRoute, useRouter } from "vue-router"
    import type { BillInput, BillApi } from "../types"
    import { CustomApiError, getErrorMessage } from "@/api"
    import BillForm from "./Form.vue"

    const bill = ref<BillInput | null>(null)
    const route = useRoute()
    const router = useRouter()
    const errorMessage = ref("")

    const props = defineProps<{
        api: BillApi
        baseUrl: string
    }>()

    const providers = ref<string[]>([])


    async function onSubmitUpdate() {
        if (!bill.value) return;

        try {
            await props.api.update(bill.value, `${route.params.id}`);
            alert("更新しました")
        } catch (error) {
            errorMessage.value = getErrorMessage(error);
        }
    }

    async function onSubmitDelete() {
        if (!bill.value) return;
        if (!confirm("削除しますか?")) return;

        try {
            await props.api.remove(`${route.params.id}`)
            alert("削除しました");
            
            await router.push(props.baseUrl);
        } catch (error) {
            if (error instanceof CustomApiError) {
                errorMessage.value = error.message;
            }
        }
    }

    onMounted(async () => {
        providers.value = await props.api.getProviderList()
        bill.value = await props.api.get(`${route.params.id}`);
    })
</script>

<template>
    <div v-if="bill">
        <BillForm 
            v-model="bill"
            :providers="providers"
            :name-error="errorMessage"
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
    </div>

</template>