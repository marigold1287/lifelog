<script setup lang="ts">
    import { ref } from "vue"
    import type { AuthorInput } from "@/features/book/author/types"
    import { validateStringEntered } from "@/validator"
    import RecordListEditor from "@/components/RecordListEditor.vue"

    const author = defineModel<AuthorInput>({ required: true })

    const props = withDefaults(defineProps<{
        submitButtonLabel?: string
        errorMessage?: string
    }>(), {
        submitButtonLabel: "Submit",
        errorMessage: "",
    })

    const emit = defineEmits<{
        submit: []
    }>()
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
        <h2>氏名</h2>
        <v-text-field
            v-model="author.name"
            :rules="[validateStringEntered]"
            label="Author name"
        />

        <h2>よみがな</h2>
        <v-text-field
            v-model="author.yomigana"
            label="よみがな"
        />
        <h3>Aliases</h3>

        <RecordListEditor
            item-key="alias"
            v-model="author.alias_records"
        />

        <h3>Note</h3>

        <v-textarea
            v-model="author.note"
        />

        <div >
            <v-btn
            prepend-icon="mdi-send"
            variant="outlined"
            type="submit"
            >
            {{ submitButtonLabel }}
            </v-btn>
        </div>
        <p v-if="errorMessage" class="error-message" style="color: red;">
            {{ errorMessage }}
        </p>

    </v-form>


</template>