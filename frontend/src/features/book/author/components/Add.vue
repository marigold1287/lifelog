<script setup lang="ts">
    import { ref } from "vue"
    import type { AuthorInput } from "@/features/book/author/types"
    import { getErrorMessage } from "@/api"
    import { create } from "../api"
    import Form from "@/features/book/author/components/Form.vue"
    import { useRouter } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()

    const author = ref<AuthorInput>({
        name: "",
        yomigana: "",
        alias_records: [{id: null, alias: ""}],
        note: ""
    })

    async function insert() {
        try {
            const record = await create(author.value);

            if (record && record.id) {
                alert("登録が完了いたしました！");
                await router.push(`/author/${record.id}`);
            }
        } catch (error) {
            errorMessage.value = getErrorMessage(error);
        }
    }
</script>

<template>
    <Form 
        v-model="author"
        @submit="insert"
        :error-message="errorMessage"
    />

</template>