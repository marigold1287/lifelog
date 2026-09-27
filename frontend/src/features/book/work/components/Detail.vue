<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import { useRoute, useRouter } from "vue-router"
    import type { WorkInput } from "../types"
    import { update, remove, get } from "../api"
    import { CustomApiError, getErrorMessage } from "@/api"
    import Form from "@/features/book/work/components/Form.vue"

    const work = ref<WorkInput | null>(null)
    const route = useRoute()
    const router = useRouter()
    const errorMessage = ref("")

    async function onSubmitUpdate() {
        if (!work.value) return;
        console.log(JSON.stringify(work.value))

        try {
            await update(work.value, `${route.params.id}`);

            alert("更新しました")
        } catch (error) {
            errorMessage.value = getErrorMessage(error);
        }
    }

    async function onSubmitDelete() {
        if (!work.value) return;
        if (!confirm("削除しますか?")) return;

        try {
            await remove(`${route.params.id}`);

            alert("削除しました");
            
            await router.push(`/work`);
        } catch (error) {
            errorMessage.value = getErrorMessage(error);
        }
    }

    onMounted(async () => {
        try {
            work.value = await get(`${route.params.id}`);
        } catch (error) {
            if (error instanceof CustomApiError) {
                alert(error.message);
            } else {
                alert("データの取得に失敗しました");
            }
        }
    })

</script>

<template>
<div v-if="work">
    <Form
        v-model="work"
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