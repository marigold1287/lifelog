<script setup lang="ts">
    import { onMounted, ref, watch } from "vue"
    import type { WorkInput, WorkView } from "../types"
    import { create } from "../api"
    import { getErrorMessage } from "@/api"
    import Form from "@/features/book/work/components/Form.vue"
    import { useRouter } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()

    const work = ref<WorkInput>({
        title: "",
        yomigana: null,
        label: "",
        label_id: null,
        publisher: "",
        publisher_id: null,
        author_records: [],
        book_records: [],
    })

    async function onsubmit() {
        if (!work.value) return;
        try {
            const record = await create(work.value);

            if (record && record.id) {
                alert("登録が完了いたしました！");
                await router.push(`/work/${record.id}`);
            }
        } catch (error) {
            errorMessage.value = getErrorMessage(error);
        }
    }

</script>

<template>
<div v-if="work">
    <Form
        v-model="work"
        :errorMessage="errorMessage"
        @submit="onsubmit"
    />
</div>

</template>