<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import type { View } from "../types.ts"
    import { getList } from "../api.ts"

    const accounts = ref<View[]>([])

    const search = ref('')
    const headers = [
        { title: '名称', key: 'label' },
        { title: '口座種類', key: 'type' },
        { title: '通貨単位', key: 'currency' },
    ]

    onMounted(async () => {
        accounts.value = await getList()
    })

</script>

<template>
    <v-card
        title="勘定項目一覧"
        flat
    >

        <RouterLink :to="'/account/add'">
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
            :items="accounts"
            :search="search"
            :headers="headers"
            :sort-by="[
                { key: 'type', order: 'asc' },
                { key: 'label', order: 'asc' },
            ]"
        >
            <template #item.label="{ item }">
                <RouterLink :to="`account/${item.id}`">
                    {{ item.label }}
                </RouterLink>
            </template>
        </v-data-table>
    </v-card>
</template>