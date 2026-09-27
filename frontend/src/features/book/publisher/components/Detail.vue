<script setup lang="ts">
    import { watch, ref } from "vue"
    import { useRoute, useRouter } from "vue-router"
    import type { PublisherInput } from "../types"
    import { getErrorMessage } from "@/api"
    import { get, getWorks, update, remove } from "../api"
    import type { WorkView } from "@/features/book/work/types"
    import BookWorkList from "@/features/book/components/BookWorkList.vue"
    import PublisherForm from "./Form.vue"

    const publisher = ref<PublisherInput | null>(null)
    const works = ref<WorkView[]>([])
    const route = useRoute()
    const router = useRouter()
    const errorMessage = ref("")
    
    async function submitUpdate() {
        if (!publisher.value) return

        try {
            console.log(publisher.value)
            await update(publisher.value, `${route.params.id}`)
            alert("更新しました")
        } catch (error) {
            console.log(getErrorMessage(error))
            errorMessage.value = getErrorMessage(error)
        }
    }

    async function submitDelete() {
        if (!publisher.value) return
        if (!confirm("削除しますか?")) return

        try {
            await remove(`${route.params.id}`)
            alert("削除しました")
            await router.push("/publisher")
        } catch (error) {
            errorMessage.value = getErrorMessage(error)
        }
    }

    watch(
        () => route.params.id,
        async (id) => {
            try {
                publisher.value = await get(`${id}`)
                works.value = await getWorks(`${id}`);
            } catch (error) {
                alert(getErrorMessage(error))
            }
        },
        { immediate: true }
    )
</script>

<template>
    <div v-if="publisher">
        <PublisherForm 
            v-model="publisher"
            :error-message="errorMessage"
            @submit="submitUpdate"
        />
        <v-btn
            class="mt-6"
            color="error"
            prepend-icon="mdi-delete"
            variant="flat"
            type="button"
            @click="submitDelete"
        >
        Delete
        </v-btn>

        <h3>作品リスト</h3>
        <BookWorkList
            :works="works"
        />

    </div>

</template>