<script setup lang="ts">
    import { watch, ref } from "vue"
    import { useRoute, useRouter } from "vue-router"
    import type { Draft } from "../types"
    import { getErrorMessage } from "@/api"
    import { get, update, remove } from "../api"
    import Form from "./Form.vue"

    const health = ref<Draft | null>(null)
    const route = useRoute()
    const router = useRouter()
    const errorMessage = ref("")
    
    async function submitUpdate() {
        if (!health.value) return

        try {
            console.log(health.value)
            await update(health.value, `${route.params.id}`)
            alert("更新しました")
        } catch (error) {
            console.log(getErrorMessage(error))
            errorMessage.value = getErrorMessage(error)
        }
    }

    async function submitDelete() {
        if (!health.value) return
        if (!confirm("削除しますか?")) return

        try {
            await remove(`${route.params.id}`)
            alert("削除しました")
            await router.push("/health")
        } catch (error) {
            errorMessage.value = getErrorMessage(error)
        }
    }

    watch(
        () => route.params.id,
        async (id) => {
            try {
                health.value = await get(`${id}`)
                console.log(health.value)
            } catch (error) {
                alert(getErrorMessage(error))
            }
        },
        { immediate: true }
    )
</script>

<template>
    <div v-if="health">
        <Form 
            v-model="health"
            :error-message="errorMessage"
            @submit="submitUpdate"
        />
        <v-btn
            class="mt-6"
            color="error"
            prepend-icon="mdi-delete"
            variant="flat"
            type="button"
            @click="submitDelete"
        >
        Delete
        </v-btn>
    </div>

</template>