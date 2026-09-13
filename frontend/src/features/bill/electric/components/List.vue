<script setup lang="ts">
import { onMounted, ref } from "vue"
import type { BillRecord } from "@/types/bill"
import { knockApi } from "@/api"

const bills = ref<BillRecord[]>([])
const search = ref('')

onMounted(async () => {
    bills.value = await knockApi<BillRecord[]>("/api/bill/electric") ?? []
})

</script>

<template>
    <v-card
        title="Electric Bill"
        flat
    >

        <RouterLink :to="'/bill/electric/add'">
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
        :items="bills"
        :search="search"
        >
            <template #item.id="{ item }">
                <RouterLink :to="`/publisher/${item.id}`">
                    {{ item.id }}
                </RouterLink>
            </template>
        </v-data-table>
    </v-card>
</template>