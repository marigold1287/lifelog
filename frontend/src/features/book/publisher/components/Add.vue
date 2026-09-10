<script setup lang="ts">
    import { ref } from "vue"
    import type { Publisher } from "@/types/book"
    import { knockApi, CustomApiError } from "@/api"
    import PublisherForm from "@/features/book/publisher/components/Form.vue"
    import { useRouter } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()

    const publisher = ref<Publisher>({
        id: null,
        name: "",
        yomigana: "",
        alias_records: [{id: null, alias: ""}],
        label_records: [{id: null, name: "レーベルなし"}]
    })

    async function insertPublisher() {
        try {
            console.log(publisher.value)
            const record = await knockApi<Publisher>(
                "/api/publisher",
                {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(publisher.value),
                },
            );

            if (record && record.id) {
                alert("登録が完了いたしました！");
                await router.push(`/publisher/${record.id}`);
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
    <PublisherForm 
        v-model="publisher"
        @submit="insertPublisher"
        :name-error="errorMessage"
    />

</template>