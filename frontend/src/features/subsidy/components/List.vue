<script setup lang="ts">
import { onMounted, ref } from "vue"
import type { View } from "../types"
import { getList } from "../api"
 	
const headers = [
  { title: '年', key: 'year' },
  { title: '給与所得控除後の金額', key: 'amount_after_salary_deductions' },
  { title: '所得税基礎控除', key: 'shotoku_zei_basic_deduction' },
  { title: '住民税基礎控除', key: 'jumin_zei_basic_deduction' },
  { title: '所得税定額控除', key: 'shotoku_zei_fixed_deduction' },
  { title: '住民税定額控除', key: 'jumin_zei_fixed_deduction' },
  { title: '市民税控除対象寄付', key: 'total_shimin_zei_deduction' },
  { title: '県民税控除対象寄付', key: 'total_kenmin_zei_deduction' },
  { title: '所得税控除対象寄付', key: 'total_shotoku_zei_deduction' },
]

const subsidies = ref<View[]>([])
const search = ref('')

onMounted(async () => {
    subsidies.value = await getList()
    console.log(subsidies.value)
})
</script>


<template>
    <v-card
        title="Subsidy"
        flat
    >

        <RouterLink :to="'/subsidy/add'">
        <v-btn>Add New</v-btn>
        </RouterLink>

        <RouterLink :to="`/subsidy/donation`">
            寄附金控除
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
        :items="subsidies"
        :search="search"
        :sort-by="[{ key: 'year', order: 'asc' }]"
        >
            <template #item.year="{ item }">
                <RouterLink :to="`/subsidy/${item.id}`">
                    {{ item.year }}
                </RouterLink>
            </template>
        </v-data-table>
    </v-card>
</template>