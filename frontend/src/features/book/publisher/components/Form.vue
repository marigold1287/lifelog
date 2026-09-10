<script setup lang="ts">
    import { validateStringEntered } from "@/validator"
    import type { Publisher } from "@/types/book"
    import RecordListEditor from "@/components/RecordListEditor.vue"

    const publisher = defineModel<Publisher>({ required: true })

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
        <h2>出版社名</h2>
        <v-text-field
            v-model="publisher.name"
            :rules="[validateStringEntered]"
            label="Publisher name"
        />

        <h2>よみがな</h2>
        <v-text-field
            v-model="publisher.yomigana"
            :rules="[validateStringEntered]"
            label="よみがな"
        />
        <h3>Aliases</h3>

        <RecordListEditor
            item-key="alias"
            v-model="publisher.alias_records"
        />


        <h3>Labels</h3>

        <RecordListEditor
            item-key="name"
            v-model="publisher.label_records"
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