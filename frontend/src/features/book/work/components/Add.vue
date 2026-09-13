<script setup lang="ts">
    import { onMounted, ref, watch } from "vue"
    import type { WorkEditRecord } from "@/types/book"
    import { knockApi, CustomApiError } from "@/api"
    import Form from "@/features/book/work/components/Form.vue"
    import { useRouter } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()

    const work = ref<WorkEditRecord>({
        id: null,
        title: "",
        label: "",
        yomigana: null,
        label_id: null,
        publisher_record: {id: null, name: ""},
        author_records: [],
        book_records: [],
    })
    watch(
        () => work.value,
        (newWork) => {
            console.log(newWork)
        },
        { deep: true }
    )


    async function create() {
        if (!work.value) return;
        try {
            const record = await knockApi<WorkEditRecord>(
                "/api/work",
                {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(work.value),
                },
            );

            if (record && record.id) {
                alert("登録が完了いたしました！");
                await router.push(`/work/${record.id}`);
            }
        } catch (error) {
            if (error instanceof CustomApiError) {
                errorMessage.value = error.message;
            } else {
                errorMessage.value = "登録に失敗しました"
            }
        }
    }

</script>

<template>
<div v-if="work">
    <Form
        v-model="work"
        :errorMessage="errorMessage"
        @submit="create"
    />
</div>

</template>