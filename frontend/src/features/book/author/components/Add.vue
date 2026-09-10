<script setup lang="ts">
    import { ref } from "vue"
    import type { Author } from "@/types/book"
    import { knockApi, CustomApiError } from "@/api"
    import Form from "@/features/book/author/components/Form.vue"
    import { useRouter } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()

    const author = ref<Author>({
        id: null,
        name: "",
        yomigana: "",
        alias_records: [{id: null, alias: ""}],
        note: ""
    })

    async function insert() {
        try {
            const record = await knockApi<Author>(
                "/api/author",
                {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(author.value),
                },
            );

            if (record && record.id) {
                alert("登録が完了いたしました！");
                await router.push(`/author/${record.id}`);
            }
        } catch (error) {
            if (error instanceof CustomApiError) {
                errorMessage.value = error.message;
            } else if (error instanceof Error) {
                errorMessage.value = error.message;
            }
        }
    }
</script>

<template>
    <Form 
        v-model="author"
        @submit="insert"
        :name-error="errorMessage"
    />

</template>