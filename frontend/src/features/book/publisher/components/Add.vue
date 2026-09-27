<script setup lang="ts">
    import { ref } from "vue"
    import type { PublisherInput } from "../types"
    import { getErrorMessage } from "@/api"
    import { create } from "../api"
    import PublisherForm from "./Form.vue"
    import { useRouter } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()

    const publisher = ref<PublisherInput>({
        name: "",
        yomigana: "",
        alias_records: [{id: null, alias: ""}],
        label_records: [{id: null, name: "レーベルなし"}]
    })

    async function submit() {
        try {
            const record = await create(publisher.value)
            console.log(record)

            if (record?.id) {
                alert("登録が完了いたしました！")
                await router.push(`/publisher/${record.id}`)
            }
        } catch (error) {
            errorMessage.value = getErrorMessage(error)
        }
    }
</script>

<template>
    <PublisherForm 
        v-model="publisher"
        @submit="submit"
        :name-error="errorMessage"
    />

</template>