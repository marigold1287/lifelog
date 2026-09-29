<script setup lang="ts">
import { onMounted, ref } from "vue"
import type { View } from "../types"
import { getList } from "../api"
import BarChart from "./BarChart.vue"

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Date', key: 'date' },
  { title: '総支給額', key: 'total_shikyu' },
  { title: '控除合計', key: 'total_kojo' },
  { title: '差引支給額', key: 'tedori' },
]

const payslips = ref<View[]>([])
const search = ref('')

onMounted(async () => {
    payslips.value = await getList()
    console.log(payslips.value)
})
</script>


<template>
    <v-card
        title="Payslip"
        flat
    >

        <RouterLink :to="'/payslip/add'">
        <v-btn>Add New</v-btn>
        </RouterLink>
        <template v-slot:text>
            <v-text-field
                v-model="search"
                label="Search"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                hide-details
                single-line
            ></v-text-field>
        </template>

        <v-data-table
        :headers="headers"
        :items="payslips"
        :search="search"
        :sort-by="[{ key: 'date', order: 'desc' }]"
        >
            <template #item.id="{ item }">
                <RouterLink :to="`/payslip/${item.id}`">
                    {{ item.id }}
                </RouterLink>
            </template>
        </v-data-table>

        <BarChart
            :payslips="payslips"
        />
    </v-card>
</template>