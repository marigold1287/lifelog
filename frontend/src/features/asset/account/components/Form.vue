<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import { validateStringEntered } from "@/validator"
    import type { Input, View } from "../types"
    import { getParentList, getAccountTypeList } from "../api";

    const account = defineModel<Input>({ required: true });
    const parents = ref<View[]>()
    const types = ref<string[]>()

    const props = withDefaults(defineProps<{
        id?: number | string | null
        submitButtonLabel?: string
        errorMessage?: string
    }>(), {
        providers: () => [],
        id: null,
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
        parents.value = await getParentList(props.id);
        types.value = await getAccountTypeList();
    })

</script>


<template>
    <v-form @submit.prevent="onSubmit" ref="form">
        <h2>名称</h2>
        <v-text-field
            v-model="account.name"
            :rules="[validateStringEntered]"
            density="compact"
        />
        <h2>通貨単位</h2>
        <v-text-field
            v-model="account.currency"
            :rules="[validateStringEntered]"
            density="compact"
        />
        <h2>勘定の種類</h2>
        <v-select
            v-model="account.type"
            :items="types"
            density="compact"
        />
        <h2>親の勘定</h2>
        <v-select
        v-model="account.parent_id"
        :items="parents"
        item-title="label"
        item-value="id"
        label="親カテゴリ"
        clearable
        />
        <h2>ソート順(番号が小さいほど先に表示される)</h2>
        <v-number-input
            v-model="account.sort_order"
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