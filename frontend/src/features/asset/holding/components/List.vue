<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import type { View } from "../types.ts"
    import { getList } from "../api.ts"

    const holdings = ref<View[]>([])

    const search = ref('')
    const headers = [
        { title: '名称', key: 'name' },
        { title: '銘柄種類', key: 'type' },
        { title: '総量', key: 'total_quantity' },
        { title: '取得コスト', key: 'acquisition_cost' },
        { title: '現在価値', key: 'current_value' },
        { title: '損益', key: 'profit_loss' },
        { title: '損益割合', key: 'profit_loss_rate' },
    ]

    onMounted(async () => {
        holdings.value = await getList()
    })

</script>

<template>
    <v-card
        title="銘柄一覧"
        flat
    >

        <RouterLink :to="'/holding/add'">
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
            :items="holdings"
            :search="search"
            :headers="headers"
        >
            <template #item.name="{ item }">
                <RouterLink :to="`holding/${item.id}`">
                    {{ item.name }}
                </RouterLink>
            </template>
        </v-data-table>
    </v-card>
</template>