<script setup lang="ts">
    import { ref, computed } from "vue"
    import type { Book } from "@/types/book"
    import type { Publisher } from "@/types/book";

    const props = defineProps<{
        books: Book[]
    }>()

    const headers = [
        { title: 'Title', key: 'title' },
        { title: 'Authors', key: 'author_records' },
        { title: 'Publisher', key: 'publisher_record' },
        { title: 'Label', key: 'label' },
        { title: 'Subtitle', key: 'subtitle' },
        { title: 'Volume', key: 'volume' },
        { title: 'Registration date', key: 'registration_date' },
        { title: 'Read date', key: 'read_date' },
    ]

    const search = ref('')

    const booksForTable = computed(() =>
        props.books.map(book => ({
            ...book,
            _searchText: [
                book.title,
                book.publisher_record.name,
                book.publisher_record.yomigana,
                book.label,
                book.registration_date,
                book.read_date,
                ...book.author_records.map(record => record.name),
                ...book.author_records.map(record => record.yomigana),
                ...book.publisher_record.alias_records.map(record => record.alias),
                ...book.author_records.flatMap(
                    record => record.alias_records.map(alias => alias.alias)
                ),
            ]
                .filter(value => value != null)
                .join(" ")
                .toLowerCase(),
        }))
    )

    const customFilter = (
        value: unknown,
        query: string,
        item?: any,
    ) => {
        if (!item) return false

        return item.raw._searchText.includes(query.toLowerCase())
    }

    const customKeySort = {
        publisher_record: (a: Publisher, b: Publisher) => a.name.localeCompare(b.name),
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
        :items="booksForTable"
        :custom-key-sort="customKeySort"
        :search="search"
        :sort-by="[{ key: 'registration_date', order: 'desc' }]"
    >
        <template #item.title="{ item }">
            <RouterLink :to="`/work/${item.work_id}`">
                {{ item.title }}
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