<script setup lang="ts">
    import { onMounted, ref, watch, computed } from "vue"
    import { validateStringEntered } from "@/validator"
    import type { TransactionDraft, EntryDraft } from "../types"
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
    const isExpense = computed(() => transaction.value.type === 'expense')

    const props = withDefaults(defineProps<{
        submitButtonLabel?: string
        errorMessage?: string
    }>(), {
        providers: () => [],
        submitButtonLabel: "Submit",
        errorMessage: "",
    })

    const EXPENSE_ACCOUNT_TYPES: AccountType[] = ["bank", "cash", "equity", "expense", "card"]

    const accountOptions = computed(() => {
        const list = isExpense.value
            ? accounts.value.filter(a => EXPENSE_ACCOUNT_TYPES.includes(a.type))
            : accounts.value
        return [...list].sort((a, b) =>
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
        const yen = isExpense.value ? yenHolding.value : undefined
        transaction.value.entries.push({
            id: null,
            account_id: null,
            holding_id: yen?.id ?? null,
            quantity: null,
            unit_price: yen ? 1 : null,
            item_name: null,
            memo: null,
        })
    }

    const isYen = (item: EntryDraft) => holdings.value.find(h => h.id === item.holding_id)?.name === '円'

    watch(
        () => transaction.value.entries.map(e => e.holding_id),
        (newIds, oldIds) => {
            transaction.value.entries.forEach((e, i) => {
            if (newIds[i] === oldIds?.[i]) return // holding_idが変わっていない行は触らない
            e.unit_price = isYen(e) ? 1 : null
            })
        }
    )


    // expense のとき、既存の全 entry を円に揃える
    // ・type が expense に変わったとき
    // ・holdings の取得が終わって yenHolding が確定したとき（初期値が expense の場合はこちら）
    watch(
        [isExpense, yenHolding],
        ([expense, yen]) => {
            if (!expense || !yen) return
            transaction.value.entries.forEach(e => {
                e.holding_id = yen.id
            })
        },
        { immediate: true }
    )
    
    watch(
        [() => transaction.value.entries.map(e => e.holding_id), holdings],
        () => {
            console.log("holding_id:", transaction.value.entries.map(e => ({
                value: e.holding_id,
                type: typeof e.holding_id,
            })))
            console.log("holdings:", holdings.value.map(h => ({
                id: h.id,
                type: typeof h.id,
                name: h.name,
            })))
        },
        { immediate: true }
    )
        


    function removeItem(index: number) {
        transaction.value.entries.splice(index, 1)
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
    })

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
                :items="accountOptions"
                item-title="label"
                item-value="id"
                label="勘定項目"
                density="compact"
            />
            <v-autocomplete
                v-if="transaction.type != 'expense'"
                v-model="item.holding_id"
                :items="holdings"
                item-title="name"
                item-value="id"
                label="銘柄"
                density="compact"
            />
            <v-text-field
                v-if="isYen(item)"
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
                v-if="!isYen(item)"
                v-model="item.unit_price"
                label="株価 or 基準価額"
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