<script setup lang="ts">
import { onMounted, ref } from "vue"
import type { Tax } from "../types"
import { getTax } from "../api"
import { formatMoney } from "@/utils/utils"
 	
const nenmatsu_headers = [
  { title: '年', key: 'year' },
  { title: '年収', key: 'nenshu' },
  { title: '社会保険料控除の合計', key: 'total_shakai_hoken_deduction' },
  { title: '課税所得', key: 'kazei_shotoku' },
  { title: '仮払所得税', key: 'paid_shotoku_zei' },
  { title: '所得税', key: 'shotoku_zei' },
  { title: '年調過不足', key: 'nenmatsu_chosei_kabusoku' },
]

const kakutei_headers = [
  { title: '年', key: 'year' },
  { title: '所得', key: 'shotoku' },
  { title: '課税所得', key: 'kazei_shotoku' },
  { title: 'ふるさと納税', key: 'furusato' },
  { title: '所得税控除寄付金', key: 'shotoku_zei_donation' },
  { title: '仮払所得税', key: 'paid_shotoku_zei' },
  { title: '所得税', key: 'shotoku_zei' },
  { title: '還付金', key: 'kanpu' },
]

const jumin_headers = [
  { title: '年', key: 'year' },
  { title: '控除総額', key: 'total_deduction' },
  { title: '課税所得', key: 'kazei_shotoku' },
  { title: '市民税', key: 'shimin_zei' },
  { title: '県民税', key: 'kenmin_zei' },
  { title: '住民税', key: 'jumin_zei' },
  { title: 'ふるさと納税上限目安', key: 'furusato_limit' },
]

const tax = ref<Tax>()

onMounted(async () => {
    tax.value = await getTax()
    console.log(tax.value)
})
</script>

<template>
    <v-card
        title="年末調整"
        flat
    >
        <v-data-table
        :headers="nenmatsu_headers"
        :items="tax?.nenmatsu_chosei"
        :sort-by="[{ key: 'year', order: 'desc' }]"
        >
        <template #item.nenshu="{ value }">{{ formatMoney(value) }}</template>
        <template #item.total_shakai_hoken_deduction="{ value }">{{ formatMoney(value) }}</template>
        <template #item.kazei_shotoku="{ value }">{{ formatMoney(value) }}</template>
        <template #item.paid_shotoku_zei="{ value }">{{ formatMoney(value) }}</template>
        <template #item.shotoku_zei="{ value }">{{ formatMoney(value) }}</template>
        <template #item.nenmatsu_chosei_kabusoku="{ value }">{{ formatMoney(value) }}</template>

        </v-data-table>
    </v-card>


    <v-card
        title="確定申告"
        flat
    >
        <v-data-table
        :headers="kakutei_headers"
        :items="tax?.kakutei_shinkoku"
        :sort-by="[{ key: 'year', order: 'desc' }]"
        >
        <template #item.shotoku="{ value }">{{ formatMoney(value) }}</template>
        <template #item.kazei_shotoku="{ value }">{{ formatMoney(value) }}</template>
        <template #item.furusato="{ value }">{{ formatMoney(value) }}</template>
        <template #item.shotoku_zei_donation="{ value }">{{ formatMoney(value) }}</template>
        <template #item.paid_shotoku_zei="{ value }">{{ formatMoney(value) }}</template>
        <template #item.shotoku_zei="{ value }">{{ formatMoney(value) }}</template>
        <template #item.kanpu="{ value }">{{ formatMoney(value) }}</template>
        </v-data-table>
    </v-card>


    <v-card
        title="住民税"
        flat
    >
        <v-data-table
        :headers="jumin_headers"
        :items="tax?.jumin_zei"
        :sort-by="[{ key: 'year', order: 'desc' }]"
        >
        <template #item.total_deduction="{ value }">{{ formatMoney(value) }}</template>
        <template #item.kazei_shotoku="{ value }">{{ formatMoney(value) }}</template>
        <template #item.shimin_zei="{ value }">{{ formatMoney(value) }}</template>
        <template #item.kenmin_zei="{ value }">{{ formatMoney(value) }}</template>
        <template #item.jumin_zei="{ value }">{{ formatMoney(value) }}</template>
        <template #item.furusato_limit="{ value }">{{ formatMoney(value) }}</template>
        </v-data-table>
    </v-card>
</template>