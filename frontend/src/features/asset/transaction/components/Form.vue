<script setup lang="ts">
    import { onMounted, ref, watch, computed } from "vue"
    import { useRoute } from 'vue-router'
    import type { TransactionDraft, EntryDraft, TxType } from "../types"
    import { getTransactionTypeList } from "../api";
    import type { View as accountView, AccountType } from "@/features/asset/account/types";
    import { getLeafList } from "@/features/asset/account/api";
    import type { View as holdingView } from "@/features/asset/holding/types";
    import { getList as getHoldingList } from "@/features/asset/holding/api";

    const transaction = defineModel<TransactionDraft>({ required: true });
    const types = ref<string[]>()
    const accounts = ref<accountView[]>([])
    const holdings = ref<holdingView[]>([])

    const yenHolding = computed(() => holdings.value.find(h => h.name === '円'))

    const props = withDefaults(defineProps<{
        submitButtonLabel?: string
        errorMessage?: string
    }>(), {
        providers: () => [],
        submitButtonLabel: "Submit",
        errorMessage: "",
    })

    const accountOptions = computed(() => {
        return [...accounts.value].sort((a, b) =>
            a.type.localeCompare(b.type) ||
            a.label.localeCompare(b.label, "ja")
        )
    })

    const totalQuantity = computed(() =>
        transaction.value.entries.reduce((sum, e) => {
            const pricePerUnits = holdings.value.find(h => h.id == e.holding_id)?.price_per_units ?? 1
            const unitPrice = e.unit_price ?? 1
            return sum + (e.quantity ?? 0) * unitPrice / pricePerUnits
        }, 0)
    )

    function addItem() {
        const yen = ["income", "expense", "transfer"].includes(transaction.value.type) ? yenHolding.value : undefined
        let account_id = null;
        if (transaction.value.entries.at(-1) !== undefined) {
            account_id = transaction.value.entries.at(-1)?.account_id || null
        }
        transaction.value.entries.push({
            id: null,
            account_id: account_id,
            holding_id: yen?.id ?? null,
            quantity: null,
            unit_price: yen ? 1 : null,
            item_name: null,
            memo: null,
        })
    }

    function removeItem(index: number) {
        transaction.value.entries.splice(index, 1)
    }


    function onAccountInput(value: accountView | string | null, index: number) {
        const selected = accounts.value.find(a => a.label == value)
        if (typeof selected !== "undefined" && typeof transaction.value.entries[index] !== "undefined") {
            transaction.value.entries[index].account_id = selected.id;
        }
    }


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
        types.value = await getTransactionTypeList();
        accounts.value = await getLeafList();
        holdings.value = await getHoldingList();
        if (transaction.value.entries.length == 0) {
            addItem()
        }
        if (transaction.value.entries.length == 0) {
            addItem()
        }
    })

    function isInputted(value: any): boolean {
        return value ? true : false
    }

</script>


<template>
    <v-form @submit.prevent="onSubmit" ref="form">
        <h2>取引日</h2>
        <v-date-input
            v-model="transaction.trade_date"
            density="compact"
        />
        <h2>取引タイプ</h2>
        <v-select
            v-model="transaction.type"
            :items="types"
            density="compact"
        />
        <h2>取引店</h2>
        <v-text-field
            v-model="transaction.shop"
            density="compact"
        />
        <h2>ノート</h2>
        <v-text-field
            v-model="transaction.note"
            density="compact"
        />

        <v-btn
            prepend-icon="mdi-plus"
            variant="outlined"
            @click="addItem"
        >
        Add Entry
        </v-btn>
        <div
            v-for="(item, index) in transaction.entries"
            :key="index"
            class="d-flex align-center mb-2"
        >
            <v-autocomplete
                v-model="item.account_id"
                :tabindex="isInputted(item.account_id) ? -1 : undefined"
                :items="accountOptions"
                item-title="label"
                item-value="id"
                label="勘定項目"
                density="compact"
                @update:search="(query) => onAccountInput(query, index)"
            />
            <v-autocomplete
                v-model="item.holding_id"
                :items="holdings"
                :tabindex="isInputted(item.holding_id) ? -1 : undefined"
                item-title="name"
                item-value="id"
                label="銘柄"
                density="compact"
            />
            <v-text-field
                v-model="item.item_name"
                label="品名"
                density="compact"
            />
            <v-number-input
                v-model="item.quantity"
                label="数量 or 価格"
                density="compact"
                control-variant="hidden"
            />
            <v-number-input
                v-model="item.unit_price"
                label="株価 or 基準価額"
                :tabindex="isInputted(item.unit_price) ? -1 : undefined"
                density="compact"
                :precision="2"
                :step="0.01"
                :min="0"
                control-variant="hidden"
            />
            <v-text-field
                v-model="item.memo"
                label="メモ"
                density="compact"
            />

            <v-btn
                icon="mdi-delete"
                variant="text"
                tabindex="-1"
                @click="removeItem(index)"
            />
        </div>

        <div class="text-h6 mt-4">
            合計: {{ totalQuantity.toLocaleString() }}
        </div>

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