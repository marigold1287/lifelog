<script setup lang="ts">
    import { ref, computed } from "vue"
    import type { Draft } from "../types"
    import CompactInputForm from "@/components/CompactInputForm.vue";

    const daily = defineModel<Draft>({ required: true })

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
        <h2>日付</h2>
        <v-date-input
            v-model="daily.date"
            density="compact"
            hide-details
        />

        <h2>体重</h2>
        <v-number-input
            v-model="daily.weight"
            :step="0.1"
            :precision="2"
            hide-details
            density="compact"
        />

        <h2>室温</h2>
        <v-number-input
            v-model="daily.room_temperature"
            :step="0.1"
            :precision="2"
            hide-details
            density="compact"
        />
        <h2>湿度</h2>
        <v-number-input
            v-model="daily.room_humidity"
            :step="0.1"
            :precision="2"
            hide-details
            density="compact"
        />
        <h2>体温</h2>
        <v-number-input
            v-model="daily.body_temperature"
            hide-details
            :step="0.1"
            :precision="2"
            density="compact"
        />
        <v-btn
        class="mt-6"
        prepend-icon="mdi-send"
        variant="outlined"
        type="submit"
        >
        {{ submitButtonLabel }}
        </v-btn>
        <p v-if="errorMessage" class="error-message" style="color: red;">
            {{ errorMessage }}
        </p>

    </v-form>


</template>