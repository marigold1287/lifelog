<script setup lang="ts">
    import { onMounted, ref, watch } from "vue"
    import { useRoute, useRouter } from "vue-router"
    import type { WorkEditRecord } from "@/types/book"
    import { knockApi, CustomApiError } from "@/api"
    import Form from "@/features/book/work/components/Form.vue"

    const work = ref<WorkEditRecord | null>(null)
    const route = useRoute()
    const router = useRouter()
    const errorMessage = ref("")

    async function update() {
        if (!work.value) return;
        console.log(JSON.stringify(work.value))

        try {
            await knockApi<WorkEditRecord>(
                `/api/work/${route.params.id}`,
                {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(work.value),
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
        if (!work.value) return;

        if (confirm("削除しますか?")) {
            try {
                await knockApi<null>(
                    `/api/work/${route.params.id}`,
                    {
                        method: "DELETE",
                    },
                );
                alert("削除しました");
                
                await router.push(`/work`);
            } catch (error) {
                if (error instanceof CustomApiError) {
                    errorMessage.value = error.message;
                }
            }
        }
    }

    onMounted(async () => {
        try {
            work.value = await knockApi<WorkEditRecord>(`/api/work/${route.params.id}`) ?? null;
            console.log(work)
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
        :errorMessage="errorMessage"
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


</div>

</template>