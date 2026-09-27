<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import type { BillView, BillApi } from "../types"
    import { billTypeLabels } from "../types"

    const bills = ref<BillView[]>([])

    const props = defineProps<{
        api: BillApi
        baseUrl: string
    }>()

    const search = ref('')
    const headers = [
    { title: 'ID', key: 'id' },
    { title: 'Start Date', key: 'start_date' },
    { title: 'End Date', key: 'end_date' },
    { title: 'Usage', key: 'usage' },
    { title: 'Total', key: 'total' },
    { title: 'Daily cost', key: 'daily_cost' },
    { title: 'Unit price', key: 'unit_price' },
    { title: 'Provider', key: 'provider'},
    ]

    onMounted(async () => {
        bills.value = await props.api.getList()
    })

</script>

<template>
    <v-card
        :title="billTypeLabels[api.type]"
        flat
    >

        <RouterLink :to="`${props.baseUrl}/add`">
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
        :headers="headers"
        >
            <template #item.id="{ item }">
                <RouterLink :to="`${props.baseUrl}/${item.id}`">
                    {{ item.id }}
                </RouterLink>
            </template>
        </v-data-table>
    </v-card>
</template>