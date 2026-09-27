<script setup lang="ts">
    import { ref, watch } from "vue"
    import type { AuthorInput } from "@/features/book/author/types"
    import { useRoute, useRouter } from "vue-router"
    import { update, remove, get, getWorks } from "../api"
    import { CustomApiError, getErrorMessage } from "@/api"
    import type { WorkView } from "@/features/book/work/types"
    import AuthorForm from "@/features/book/author/components/Form.vue"
    import BookWorkList from "@/features/book/components/BookWorkList.vue"

    const author = ref<AuthorInput | null>(null)
    const works = ref<WorkView[]>([])
    const route = useRoute()
    const router = useRouter()
    const errorMessage = ref("")

    async function onSubmitUpdate() {
        if (!author.value) return;

        try {
            await update(author.value, `${route.params.id}`);

            alert("更新しました")
        } catch (error) {
            errorMessage.value = getErrorMessage(error);
        }
    }

    async function onSubmitDelete() {
        if (!author.value) return;
        if (!confirm("削除しますか?")) return;

        try {
            await remove(`${route.params.id}`);
            alert("削除しました");
            
            await router.push(`/author`);
        } catch (error) {
            errorMessage.value = getErrorMessage(error);
        }
    }

    watch(
        () => route.params.id,
        async () => {
            try {
                author.value = await get(`${route.params.id}`);
                works.value = await getWorks(`${route.params.id}`);
            } catch (error) {
                if (error instanceof CustomApiError) {
                    alert(error.message);
                } else {
                    alert("データの取得に失敗しました");
                }
            }
        },
        { immediate: true }
    )

</script>

<template>
    <div v-if="author">
        <AuthorForm 
            v-model="author"
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

        <h3>作品リスト</h3>

        <BookWorkList
            :works="works"
        />

    </div>

</template>