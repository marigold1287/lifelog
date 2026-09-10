<script setup lang="ts">
    import { validateStringEntered } from "@/validator"
    import type { Author } from "@/types/book"
    import RecordListEditor from "@/components/RecordListEditor.vue"

    const author = defineModel<Author>({ required: true })

    const emit = defineEmits<{
        submit: []
    }>()
    const props = withDefaults(defineProps<{
        submitButtonLabel?: string
        errorMessage?: string
    }>(), {
        submitButtonLabel: "Submit",
        errorMessage: "",
    })

</script>


<template>
    <v-form @submit.prevent="emit('submit')">
        <h2>氏名</h2>
        <v-text-field
            v-model="author.name"
            :rules="[validateStringEntered]"
            label="Author name"
        />

        <h2>よみがな</h2>
        <v-text-field
            v-model="author.yomigana"
            :rules="[validateStringEntered]"
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