<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import type { TransactionView } from "../types.ts"
    import { getList } from "../api.ts"

    const transactions = ref<TransactionView[]>([])

    const search = ref('')
    const headers = [
        { title : 'ID', key: 'id'},
        { title: '取引日', key: 'trade_date' },
        { title: '取引店', key: 'shop' },
        { title: '取引タイプ', key: 'type' },
        { title: 'ノート', key: 'note' },
    ]

    onMounted(async () => {
        transactions.value = await getList()
    })

</script>

<template>
    <v-card
        title="取引一覧"
        flat
    >

        <RouterLink :to="'/transaction/add'">
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
            :items="transactions"
            :search="search"
            :headers="headers"
        >
            <template #item.id="{ item }">
                <RouterLink :to="`transaction/${item.id}`">
                    {{ item.id }}
                </RouterLink>
            </template>
        </v-data-table>
    </v-card>
</template>