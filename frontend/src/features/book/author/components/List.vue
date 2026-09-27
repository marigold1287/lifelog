<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import type { AuthorView } from "@/features/book/author/types"
    import { getList} from "../api"
    import { customFilter } from "@/features/book/author/scripts.ts"

    const headers = [
        { title: 'ID', key: 'id' },
        { title: 'Name', key: 'name' },
        { title: 'よみがな', key: 'yomigana' },
    ]

    const authors = ref<AuthorView[]>([])
    const search = ref('')

    onMounted(async () => {
        authors.value = await getList()
    })

</script>


<template>
    <v-card
        title="Author"
        flat
    >

        <RouterLink :to="'/author/add'">
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
        :custom-filter="customFilter"
        :items="authors"
        :search="search"
        >
            <template #item.id="{ item }">
                <RouterLink :to="`/author/${item.id}`">
                    {{ item.id }}
                </RouterLink>
            </template>
        </v-data-table>
    </v-card>
</template>