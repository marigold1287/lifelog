<script setup lang="ts">
    import { onMounted, ref, watch, computed } from "vue"
    import { useRoute, useRouter } from "vue-router"
    import { get, update, remove } from "../api.ts"
    import { BASE_URL } from "../router.ts"
    import type { Input } from "../types.ts"
    import { CustomApiError, getErrorMessage } from "@/api"
    import Form from "./Form.vue"

    const account = ref<Input | null>(null)
    const route = useRoute()
    const router = useRouter()
    const errorMessage = ref("")

    async function onSubmitUpdate() {
        if (!account.value) return;

        try {
            await update(account.value, `${route.params.id}`);
            alert("更新しました")
        } catch (error) {
            errorMessage.value = getErrorMessage(error);
        }
    }

    async function onSubmitDelete() {
        if (!account.value) return;
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
        account.value = await get(`${route.params.id}`);
        console.log(account.value)
    })
</script>

<template>
    <div v-if="account">
        <Form 
            v-model="account"
            :id="`${route.params.id}`"
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
    </div>

</template>