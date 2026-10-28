<script setup lang="ts">
    import { computed, ref, watch } from "vue"
    import type { AccountSummary,EntryResponse } from "../types.ts"
    import { get, getEntries } from "../api.ts"
    import { formatMoney } from "@/utils/utils.ts"


    import AccountTree from "./AccountTree.vue"

    const now = new Date()

    const selectedYear = ref(now.getFullYear())
    const selectedMonth = ref(now.getMonth() + 1)

    const summary = ref<AccountSummary | null>(null)
    const entries = ref<EntryResponse[]>([])
    const kakeiboEntries = ref<EntryResponse[]>([])
    const transferEntries = ref<EntryResponse[]>([])
    const tradingEntries = ref<EntryResponse[]>([])
    const loading = ref(false)
    const error = ref("")
    const kakeiboSearch = ref('')
    const transferSearch = ref('')
    const tradingSearch = ref('')

    const header = [
        { title: '取引日', key: 'trade_date' },
        { title: '店', key: 'shop' },
        { title: 'ノート', key: 'note' },
        { title: '勘定', key: 'account' },
        // { title: '銘柄', key: 'holding' },
        { title: '品名', key: 'item_name' },
        { title: '価格', key: 'quantity' },
        { title: 'メモ', key: 'memo' },
    ]
    const tradingHeader = [
        { title: '取引日', key: 'trade_date' },
        { title: '店', key: 'shop' },
        { title: '銘柄', key: 'holding' },
        { title: '価格', key: 'quantity' },
        { title: '基準価額', key: 'unit_price' },
    ]


    const years = computed(() =>
      Array.from(
        { length: now.getFullYear() - 2016 + 1 },
        (_, i) => 2016 + i
      ).reverse()
    )

    const months: (number | null)[] = [
      null, ...Array.from({ length: 12 }, (_, i) => i + 1)
    ]

    let requestId = 0

    async function loadSummary() {
        const id = ++requestId

        loading.value = true
        error.value = ""

        try {
            const result = await get(
                selectedYear.value,
                selectedMonth.value,
            )
            const entry_result = await getEntries(
                selectedYear.value,
                selectedMonth.value,
            )

            // 古いリクエストの結果で表示を上書きしない
            if (id === requestId) {
                summary.value = result
                entries.value = entry_result
                kakeiboEntries.value = entry_result.filter(e => e.account_type == "income" || e.account_type == "expense");
                transferEntries.value = entry_result.filter(e => e.transaction_type == "transfer" && e.quantity > 0)
                tradingEntries.value = entry_result.filter(e => e.holding_type == "fund" || e.holding_type == "stock")
            }
        } catch (e) {
                if (id === requestId) {
                error.value = "データの取得に失敗しました。"
                console.error(e)
            }
        } finally {
            if (id === requestId) {
                loading.value = false
            }
        }
    }

    watch(
        [selectedYear, selectedMonth],
        () => {
            void loadSummary()
        },
        { immediate: true },
    )
</script>

<template>
  <main class="page">
    <header class="page-header">
      <div>
        <h1>家計簿</h1>

        <RouterLink :to="'/transaction/add'">
        <v-btn>Add New</v-btn>
        </RouterLink>
        <p class="subtitle">収支のサマリー</p>
      </div>

      <div class="period-selector">
        <select v-model.number="selectedYear" aria-label="年">
          <option
            v-for="year in years"
            :key="year"
            :value="year"
          >
            {{ year }}年
          </option>
        </select>

      <select v-model="selectedMonth" aria-label="月">
        <option :value="null">年間</option>
        <option
          v-for="month in months.filter(m => m !== null)"
          :key="month"
          :value="month"
        >
          {{ month }}月
        </option>
      </select>
      </div>
    </header>

    <p v-if="loading" class="status">
      データを読み込み中...
    </p>

    <p v-else-if="error" class="error">
      {{ error }}
    </p>

    <template v-else-if="summary">
      <section class="summary-grid">
        <article class="summary-card expense-card">
          <p>支出合計</p>
          <strong>{{ formatMoney(summary.expense_total) }}</strong>
        </article>

        <article class="summary-card income-card">
          <p>収入合計</p>
          <strong>{{ formatMoney(summary.income_total) }}</strong>
        </article>

        <article class="summary-card balance-card">
          <p>収支</p>
          <strong>{{ formatMoney(summary.total) }}</strong>
        </article>
      </section>

      <section class="category-section">
        <h2>支出の内訳</h2>

        <div v-if="summary.expense.length" class="category-panel">
          <AccountTree :nodes="summary.expense" />
        </div>
        <p v-else class="empty">支出データはありません。</p>
      </section>

      <section class="category-section">
        <h2>収入の内訳</h2>

        <div v-if="summary.income.length" class="category-panel">
          <AccountTree :nodes="summary.income" />
        </div>
        <p v-else class="empty">収入データはありません。</p>
      </section>


      <v-card title="支出/収入一覧" flat>
        <template #text>
          <v-text-field
            v-model="kakeiboSearch"
            label="Search"
            prepend-inner-icon="mdi-magnify"
            variant="outlined"
            hide-details
            single-line
          />
        </template>

        <v-data-table
          :items="kakeiboEntries"
          :search="kakeiboSearch"
          :headers="header"
        >
          <template #item.trade_date="{ item }">
            <RouterLink :to="`/transaction/${item.transaction_id}`">
              {{ item.trade_date }}
            </RouterLink>
          </template>

          <template #item.quantity="{ value }">{{ formatMoney(value) }}</template>
        </v-data-table>
      </v-card>


      <v-card title="振替一覧" flat>
        <template #text>
          <v-text-field
            v-model="transferSearch"
            label="Search"
            prepend-inner-icon="mdi-magnify"
            variant="outlined"
            hide-details
            single-line
          />
        </template>

        <v-data-table
          :items="transferEntries"
          :search="transferSearch"
          :headers="header"
        >
          <template #item.trade_date="{ item }">
            <RouterLink :to="`/transaction/${item.transaction_id}`">
              {{ item.trade_date }}
            </RouterLink>
          </template>

          <template #item.quantity="{ value }">{{ formatMoney(value) }}</template>
        </v-data-table>
      </v-card>


      <v-card title="株式取引一覧" flat>
        <template #text>
          <v-text-field
            v-model="tradingSearch"
            label="Search"
            prepend-inner-icon="mdi-magnify"
            variant="outlined"
            hide-details
            single-line
          />
        </template>

        <v-data-table
          :items="tradingEntries"
          :search="tradingSearch"
          :headers="tradingHeader"
        >
          <template #item.trade_date="{ item }">
            <RouterLink :to="`/transaction/${item.transaction_id}`">
              {{ item.trade_date }}
            </RouterLink>
          </template>

          <template #item.quantity="{ value }">{{ formatMoney(value) }}</template>
          <template #item.unit_price="{ value }">{{ formatMoney(value) }}</template>
        </v-data-table>
      </v-card>


    </template>
  </main>
</template>

<style scoped>
.page {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px 16px 48px;
  color: var(--text-color, #1f2937);
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
}

h1 {
  margin: 0;
  font-size: 1.7rem;
  color: var(--text-color, #f6f6f6);
}

.subtitle {
  margin: 6px 0 0;
  color: #888;
  font-size: 0.9rem;
}

.period-selector {
  display: flex;
  gap: 8px;
}

.period-selector select {
  padding: 10px 12px;
  border: 1px solid var(--border-color, #d1d5db);
  border-radius: 8px;
  background: var(--surface-color, white);
  color: inherit;
  font: inherit;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 32px;
}

.summary-card {
  min-width: 0;
  padding: 20px;
  border: 1px solid var(--border-color, #e5e7eb);
  border-radius: 14px;
  background: var(--surface-color, white);
}

.summary-card p {
  margin: 0 0 12px;
  color: #777;
  font-size: 0.9rem;
}

.summary-card strong {
  display: block;
  overflow-wrap: anywhere;
  font-size: clamp(1.05rem, 2.5vw, 1.55rem);
  font-variant-numeric: tabular-nums;
}

.expense-card {
  border-top: 4px solid #e87979;
}

.income-card {
  border-top: 4px solid #54a987;
}

.balance-card {
  border-top: 4px solid #7296d4;
}

.category-section {
  margin-top: 30px;
}

.category-section h2 {
  margin-bottom: 14px;
  font-size: 1.2rem;
  color: var(--text-color, #f6f6f6);
}

.category-panel {
  overflow: hidden;
  border: 1px solid var(--border-color, #e5e7eb);
  border-radius: 12px;
  background: var(--surface-color, white);
}

.status,
.empty {
  padding: 20px;
  color: #888;
  text-align: center;
}

.error {
  padding: 16px;
  border-radius: 8px;
  background: #fef2f2;
  color: #b91c1c;
}

@media (max-width: 600px) {
  .page {
    padding: 18px 12px 32px;
  }

  .summary-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .summary-card {
    padding: 15px 16px;
  }

  .summary-card p {
    margin-bottom: 6px;
  }
}
</style>
