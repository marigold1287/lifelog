<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import { validateStringEntered } from "@/validator"
    import type { Input, View } from "../types"

    const holding = defineModel<Input>({ required: true });
    const parents = ref<View[]>()

    const props = withDefaults(defineProps<{
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


  price_source: string | null
  price_per_units: number
<template>
    <v-form @submit.prevent="onSubmit" ref="form">
        <h2>名称</h2>
        <v-text-field
            v-model="holding.name"
            :rules="[validateStringEntered]"
            density="compact"
        />
        <h2>通貨単位</h2>
        <v-text-field
            v-model="holding.currency"
            :rules="[validateStringEntered]"
            density="compact"
        />
        <h2>シンボル/ティッカー</h2>
        <v-text-field
            v-model="holding.symbol"
            density="compact"
        />
        <h2>種類</h2>
        <v-select
            v-model="holding.type"
            :items="['cash', 'fund', 'stock']"
            density="compact"
        />
        <h2>株価/基準価額のソース</h2>
        <v-select
            v-model="holding.price_source"
            :items="['ufj', 'rakuten', 'nissei', 'yfinance']"
            density="compact"
        />
        <h2>価格単位</h2>
        <v-number-input
            v-model="holding.price_per_units"
            density="compact"
        />
        <div >
            <v-btn
            class="mt-4"
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