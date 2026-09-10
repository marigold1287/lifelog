<script setup lang="ts">
    import { watch, ref } from "vue"
    import { useRoute, useRouter } from "vue-router"
    import type { PublisherDetail } from "@/types/book"
    import { knockApi, CustomApiError } from "@/api"
    import BookWorkList from "@/components/BookWorkList.vue"
    import PublisherForm from "@/features/book/publisher/components/Form.vue"

    const publisher = ref<PublisherDetail | null>(null)
    const route = useRoute()
    const router = useRouter()
    const errorMessage = ref("")

    const headers = [
        { title: 'ID', key: 'id' },
        { title: 'Title', key: 'title' },
        { title: 'Authors', key: 'author_records' },
        { title: 'Publisher', key: 'publisher' },
        { title: 'Label', key: 'label' },
    ]


    async function fetchPublisher() {
        const publisher = await knockApi<PublisherDetail>(
            `/api/publisher/${route.params.id}`
        );

        console.log(publisher)

        if (!publisher) {
            throw new Error("出版社データがありません");
        }

        return publisher;
    }

    async function updatePublisher() {
        if (!publisher.value) return;

        try {
            await knockApi<PublisherDetail>(
                `/api/publisher/${route.params.id}`,
                {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(publisher.value),
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
        if (!publisher.value) return;

        if (confirm("削除しますか?")) {
            try {
                await knockApi<null>(
                    `/api/publisher/${route.params.id}`,
                    {
                        method: "DELETE",
                    },
                );
                alert("削除しました");
                
                await router.push(`/publisher`);
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
                publisher.value = await fetchPublisher();
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
    <div v-if="publisher">
        <PublisherForm 
            v-model="publisher"
            :name-error="errorMessage"
            @submit="updatePublisher"
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
            :works="publisher.work_records"
        />

    </div>

</template>