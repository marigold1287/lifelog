<script setup lang="ts">
    import { ref, computed } from "vue"
    import type { Input } from "../types"
    import CompactInputForm from "@/components/CompactInputForm.vue";

    const subsidy = defineModel<Input>({ required: true })

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
        <h2>年</h2>
        <v-number-input
            v-model="subsidy.year"
            density="compact"
            hide-details
        />
        <h2>給与所得控除後の金額</h2>
        <v-number-input
            v-model="subsidy.amount_after_salary_deductions"
            density="compact"
            hide-details
        />
        <h2>所得税基礎控除</h2>
        <v-number-input
            v-model="subsidy.shotoku_zei_basic_deduction"
            density="compact"
            hide-details
        />
        <h2>住民税基礎控除</h2>
        <v-number-input
            v-model="subsidy.jumin_zei_basic_deduction"
            density="compact"
            hide-details
        />
        <h2>所得税定額控除</h2>
        <v-number-input
            v-model="subsidy.shotoku_zei_fixed_deduction"
            density="compact"
            hide-details
        />
        <h2>住民税定額控除</h2>
        <v-number-input
            v-model="subsidy.jumin_zei_fixed_deduction"
            density="compact"
            hide-details
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