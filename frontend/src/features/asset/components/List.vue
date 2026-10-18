<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import type { AssetView } from "../types"
    import { getAssetList } from "../api"
    import AreaChart from "./AreaChart.vue"

    const assets = ref<AssetView[]>([])

    const search = ref('')
    const headers = [
    { title: '日付', key: 'date' },
    { title: '現金', key: 'cash' },
    { title: '投資信託', key: 'fund' },
    { title: '株式', key: 'stock' },
    { title: '年金', key: 'pension' },
    { title: 'Total', key: 'total' },
    ]

    onMounted(async () => {
        assets.value = await getAssetList()
    })

</script>

<template>
    <v-card
        title="資産推移"
        flat
    >
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
            :items="assets"
            :search="search"
            :headers="headers"
        >
        </v-data-table>

        <AreaChart
            :assets="assets"
        />

    </v-card>
</template>