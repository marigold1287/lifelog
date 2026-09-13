<script setup lang="ts">
    import { ref, computed, onMounted } from "vue"
    import { knockApi } from "@/api";
    import type { Book, Publisher, Author } from "@/types/book"

    const props = defineProps<{
        books: Book[]
    }>()

    const authors = ref<Author[]>([])
    const publishers = ref<Publisher[]>([])

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

    const publisherMap = computed(() =>
        new Map(publishers.value.map(publisher => [publisher.id, publisher]))
    )

    const authorMap = computed(() =>
        new Map(authors.value.map(author => [author.id, author]))
    )

    const search = ref('')
    const booksForTable = computed(() =>
        props.books.map(book => {
            const publisher = publisherMap.value.get(book.publisher_id)

            const bookAuthors = book.author_ids
                .map(id => authorMap.value.get(id))
                .filter((author): author is Author => author != null)


            return {
                ...book,
                publisher_record: publisher,
                author_records: bookAuthors,
                _searchText: [
                    book.title,
                    book.yomigana,
                    publisher?.name,
                    publisher?.yomigana,
                    book.label,
                    book.registration_date,
                    book.read_date,
                    ...bookAuthors.map(record => record.name),
                    ...bookAuthors.map(record => record.yomigana),
                    ...(publisher?.alias_records ?? []).map(record => record.alias),
                    ...bookAuthors.flatMap(
                        record => record.alias_records.map(alias => alias.alias)
                    )
                ]
                    .filter(value => value != null)
                    .join(" ")
                    .toLowerCase(),
            }
        })
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

    onMounted(async () => {
        authors.value = await knockApi<Author[]>("/api/author") ?? []
        publishers.value = await knockApi<Publisher[]>("/api/publisher") ?? []
    })

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
                key="author.name"
            >
                <RouterLink :to="`/author/${author.id}`">
                    {{ author.name }}
                </RouterLink>{{ index < item.author_records.length - 1 ? ', ' : '' }}
            </template>
        </template>

        <template #item.publisher_record="{ item }">
            <RouterLink :to="`/publisher/${item.publisher_record?.id}`">
                {{ item.publisher_record?.name }}
            </RouterLink>
        </template>
    </v-data-table>
</template>