<script setup lang="ts">
    import { onMounted, ref, watch } from "vue"
    import { useRoute, useRouter } from "vue-router"
    import type { AuthorDetail } from "@/types/book"
    import { knockApi, CustomApiError } from "@/api"
    import AuthorForm from "@/features/book/author/components/Form.vue"
    import BookWorkList from "@/components/BookWorkList.vue"

    const author = ref<AuthorDetail | null>(null)
    const route = useRoute()
    const router = useRouter()
    const errorMessage = ref("")


    async function get() {
        const author = await knockApi<AuthorDetail>(
            `/api/author/${route.params.id}`
        );

        if (!author) {
            throw new Error("著者データがありません");
        }

        console.log(author)

        return author;
    }

    async function update() {
        if (!author.value) return;

        try {
            await knockApi<AuthorDetail>(
                `/api/author/${route.params.id}`,
                {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(author.value),
                },
            );

            alert("更新しました")
        } catch (error) {
            if (error instanceof CustomApiError) {
                errorMessage.value = error.message;
            } else {
                errorMessage.value = "更新に失敗しました"
            }
        }
    }

    async function confirmDelete() {
        if (!author.value) return;

        if (confirm("削除しますか?")) {
            try {
                await knockApi<null>(
                    `/api/author/${route.params.id}`,
                    {
                        method: "DELETE",
                    },
                );
                alert("削除しました");
                
                await router.push(`/author`);
            } catch (error) {
                if (error instanceof CustomApiError) {
                    errorMessage.value = error.message;
                }
            }
        }
    }

    watch(
        () => route.params.id,
        async () => {
            try {
                author.value = await get();
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
            :name-error="errorMessage"
            @submit="update"
        />
        <v-btn
            class="mt-6"
            color="error"
            prepend-icon="mdi-delete"
            variant="flat"
            type="button"
            @click="confirmDelete"
        >
        Delete
        </v-btn>

        <h3>作品リスト</h3>

        <BookWorkList
            :works="author.work_records"
        />

    </div>

</template>