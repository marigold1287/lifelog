<script setup lang="ts">
    import { ref } from "vue"
    import { validateStringEntered } from "@/validator"
    import type { BillInput } from "../types"

    const bill = defineModel<BillInput>({ required: true })

    const props = withDefaults(defineProps<{
        providers?: string[]
        submitButtonLabel?: string
        errorMessage?: string
    }>(), {
        providers: () => [],
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
        <h2>開始日</h2>
        <v-date-input
            v-model="bill.start_date"
            label="開始日"
            density="compact"
            hide-details
        />

        <h2>終了日</h2>
        <v-date-input
            v-model="bill.end_date"
            label="終了日"
            density="compact"
            hide-details
        />

        <h2>合計金額</h2>
        <v-number-input
            v-model="bill.total"
            label="合計金額"
            density="compact"
            hide-details
        />

        <h2>使用量</h2>
        <v-number-input
            v-model="bill.usage"
            label="使用量"
            density="compact"
            hide-details
        />

        <h2>供給会社</h2>
        <v-combobox
            v-model="bill.provider"
            :items="props.providers"
            label="供給会社"
            :rules="[validateStringEntered]"
            density="compact"
            hide-details
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