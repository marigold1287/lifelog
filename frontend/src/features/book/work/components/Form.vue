<script setup lang="ts">
    import {ref} from "vue"
    import type { WorkEditRecord } from "@/types/book"
    import { validateStringEntered } from "@/validator"
    import AuthorEditor from "@/features/book/work/components/AuthorEditor.vue"
    import BookEditor from "@/features/book/work/components/BookEditor.vue"
    import PublisherLabelEditor from "@/features/book/work/components/PublisherLabelEditor.vue"

    const work = defineModel<WorkEditRecord>({ required: true })

    const emit = defineEmits<{
        submit: []
    }>()

    const props = withDefaults(defineProps<{
        errorMessage?: string
    }>(), {
        errorMessage: "",
    })

    const form = ref()

    async function onSubmit() {
        const { valid } = await form.value.validate()

        if (!valid) {
            return
        }

        emit("submit")
    }


</script>


<template>
    <v-form @submit.prevent="onSubmit" ref="form">
        <h2>タイトル</h2>
        <v-text-field
            v-model="work.title"
            :rules="[validateStringEntered]"
            label="書籍名"
        />

        <h2>著者</h2>
        <AuthorEditor
            v-model="work.author_records"
        />

        <h2>出版社/レーベル</h2>
        <PublisherLabelEditor 
            v-model:publisher="work.publisher_record" 
            v-model:label="work.label" 
            v-model:label-id="work.label_id" 
        />

        <h2>書籍リスト</h2>
        <BookEditor
            v-model="work.book_records"
        />

        <div >
            <v-btn
            prepend-icon="mdi-send"
            variant="outlined"
            type="submit"
            >
            Submit
            </v-btn>
        </div>
        
        <p v-if="errorMessage" class="error-message" style="color: red;">
            {{ errorMessage }}
        </p>
    </v-form>
</template>