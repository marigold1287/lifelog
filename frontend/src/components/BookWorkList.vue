<script setup lang="ts">
    import { ref } from "vue"
    import type { WorkRecord, Publisher, Author } from "@/types/book"

    const props = defineProps<{
        works: WorkRecord[]
    }>()

    const headers = [
        { title: 'ID', key: 'id' },
        { title: 'Title', key: 'title' },
        { title: 'Authors', key: 'author_records' },
        { title: 'Publisher', key: 'publisher_record' },
        { title: 'Label', key: 'label' },
    ]

    const search = ref('')

    const customFilter = (
        value: unknown,
        query: string,
        item?: any,
    ) => {
        if (!item) return false

        const work = item.raw as WorkRecord

        const text = [
            work.id,
            work.title,
            work.yomigana,
            work.publisher_record.name,
            work.publisher_record.yomigana,
            work.label,
            ...work.author_records.map(record => record.name),
            ...work.author_records.map(record => record.yomigana),
            ...work.publisher_record.alias_records.map(record => record.alias),
            ...work.author_records.flatMap(record => record.alias_records.map(alias => alias.alias)),
        ]
        .filter(value => value != null)
        .join(" ")

        return text.toLowerCase().includes(query.toLowerCase())
    }

    const customKeySort = {
        publisher_record: (a: Publisher, b: Publisher) => a.name.localeCompare(b.name),
        author_records: (a: Author[], b: Author[]) => {
            const aNames = [...a]
                .sort((x, y) => x.name.localeCompare(y.name, "ja"))
                .map(author => author.name)
                .join(", ")

            const bNames = [...b]
                .sort((x, y) => x.name.localeCompare(y.name, "ja"))
                .map(author => author.name)
                .join(", ")

            return aNames.localeCompare(bNames, "ja")
        },
        title: (a: string, b: string) => a.localeCompare(b, "ja"),
    }

</script>

<template>
    <v-text-field
        v-model="search"
        label="Search"
        prepend-inner-icon="mdi-magnify"
        variant="outlined"
        hide-details
        single-line
    />

    <v-data-table
        :headers="headers"
        :custom-filter="customFilter"
        :items="works"
        :search="search"
        :custom-key-sort="customKeySort"
    >
        <template #item.id="{ item }">
            <RouterLink :to="`/work/${item.id}`">
                {{ item.id }}
            </RouterLink>
        </template>

        <template #item.author_records="{ item }">
            <template
                v-for="(author, index) in item.author_records"
                :key="author.id"
            >
                <RouterLink :to="`/author/${author.id}`">
                    {{ author.name }}
                </RouterLink>{{ index < item.author_records.length - 1 ? ', ' : '' }}
            </template>
        </template>

        <template #item.publisher_record="{ item }">
            <RouterLink :to="`/publisher/${item.publisher_record.id}`">
                {{ item.publisher_record.name }}
            </RouterLink>
        </template>
    </v-data-table>
</template>