<script setup lang="ts">
import { onMounted, ref } from "vue"
import type { View } from "../types"
import { getList } from "../api"
 	
const headers = [
  { title: 'ID', key: 'entry_id' },
  { title: '寄付日', key: 'trade_date' },
  { title: '控除年', key: 'deduction_year' },
  { title: '寄付先', key: 'shop' },
  { title: '市民税控除の対象', key: 'is_shimin_zei_deduction' },
  { title: '県民税控除の対象', key: 'is_kenmin_zei_deduction' },
  { title: '所得税控除の対象', key: 'is_shotoku_zei_deduction' },
]

const deductions = ref<View[]>([])
const search = ref('')

onMounted(async () => {
    deductions.value = await getList()
    console.log(deductions.value)
})
</script>


<template>
    <v-card
        title="Subsidy(Donation Deduction)"
        flat
    >

        <RouterLink :to="'/subsidy/donation/add'">
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
        :items="deductions"
        :search="search"
        >
            <template #item.entry_id="{ item }">
                <RouterLink :to="`/subsidy/donation/${item.entry_id}`">
                    {{ item.entry_id }}
                </RouterLink>
            </template>
        </v-data-table>
    </v-card>
</template>