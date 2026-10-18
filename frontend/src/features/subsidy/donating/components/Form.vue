<script setup lang="ts">
    import { ref, computed, onMounted } from "vue"
    import type { Draft, EntrySchema } from "../types"
    import { getEntriesWithoutDonationDeduction } from "../api";

    const deduction = defineModel<Draft>({ required: true })
    const entries = ref<EntrySchema[]>([])

    const props = withDefaults(defineProps<{
        entry_id?: string | number | null
        submitButtonLabel?: string
        errorMessage?: string
    }>(), {
        entry_id: null,
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

    onMounted(async () => {
        entries.value = await getEntriesWithoutDonationDeduction(props.entry_id);
        console.log(entries.value)
    })


</script>

<template>
    <v-form @submit.prevent="onSubmit" ref="form">
        <h2>対象エントリー</h2>
        <v-select
            v-model="deduction.entry_id"
            :items="entries"
            item-title="label"
            item-value="id"
            hide-details
        />
        <h2>控除対象年</h2>
        <v-number-input
            v-model="deduction.deduction_year"
            density="compact"
            hide-details
        />
        <h2>市民税控除の対象の場合はチェック</h2>
        <v-checkbox
            v-model="deduction.is_shimin_zei_deduction"
            density="compact"
            hide-details
        />
        <h2>県民税控除の対象の場合はチェック</h2>
        <v-checkbox
            v-model="deduction.is_kenmin_zei_deduction"
            density="compact"
            hide-details
        />
        <h2>所得税控除の対象の場合はチェック</h2>
        <v-checkbox
            v-model="deduction.is_shotoku_zei_deduction"
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