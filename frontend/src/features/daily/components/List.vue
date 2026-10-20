<script setup lang="ts">
import { onMounted, ref } from "vue"
import type { Response } from "../types"
import { getList } from "../api"
import Chart from "./Chart.vue"

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Date', key: 'date' },
  { title: '総支給額', key: 'total_shikyu' },
  { title: '控除合計', key: 'total_kojo' },
  { title: '差引支給額', key: 'tedori' },
]

const dailys = ref<Response[]>([])
const search = ref('')

onMounted(async () => {
    dailys.value = await getList()
    console.log(dailys.value)
})
</script>


<template>
    <v-card
        title="デイリーログ"
        flat
    >

        <RouterLink :to="'/daily/add'">
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
        :items="dailys"
        :search="search"
        :sort-by="[{ key: 'date', order: 'desc' }]"
        >
            <template #item.id="{ item }">
                <RouterLink :to="`/daily/${item.id}`">
                    {{ item.id }}
                </RouterLink>
            </template>
        </v-data-table>

        <Chart
            :data="dailys"
            data_name="weight"
        ></Chart>

    </v-card>
</template>