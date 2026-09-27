<script setup lang="ts">
    import { ref, computed, onMounted } from "vue"
    import { knockApi } from "@/api";
    import type { PublisherView } from "@/features/book/publisher/types"
    import type { BookView } from "@/features/book/book/types";
    import type { AuthorView } from "@/features/book/author/types";
    import { generateAuthorMap, generateSearchText as generateAuthorSearchText } from "@/features/book/author/scripts";
    import { generatePublisherMap, generateSearchText as generatePublisherSearchText } from "@/features/book/publisher/scripts";

    const props = defineProps<{
        books: BookView[]
    }>()

    const authors = ref<AuthorView[]>([])
    const publishers = ref<PublisherView[]>([])

    const headers = [
        { title: 'Title', key: 'title' },
        { title: 'Authors', key: 'author_records' },
        { title: 'Publisher', key: 'publisher' },
        { title: 'Label', key: 'label' },
        { title: 'Subtitle', key: 'subtitle' },
        { title: 'Volume', key: 'volume' },
        { title: 'Registration date', key: 'registration_date' },
        { title: 'Read date', key: 'read_date' },
    ]

    const publisherMap = computed(() =>
        generatePublisherMap(publishers.value)
    )

    const labelMap = computed(() =>
        new Map(
            publishers.value.flatMap(publisher => publisher.label_records)
                .map(label => [label.id, label])
        )
    )

    const authorMap = computed(() =>
        generateAuthorMap(authors.value)
    )

    const search = ref('')
    const booksForTable = computed(() =>
        props.books.map(book => {
            const publisher = publisherMap.value.get(book.publisher_id)
            const label = labelMap.value.get(book.label_id)

            const bookAuthors = book.author_ids
                .map(id => authorMap.value.get(id))
                .filter((author): author is AuthorView => author != null)

            const authorFilterText = bookAuthors
                .map(author => generateAuthorSearchText(author))
                .join(" ")

            const publisherFilterText = publisher
                ? generatePublisherSearchText(publisher)
                : null

            return {
                ...book,
                publisher: publisher?.name,
                publisher_id: publisher?.id,
                author_records: bookAuthors,
                label: label?.name,
                _searchText: [
                    book.title,
                    book.yomigana,
                    label?.name,
                    book.registration_date,
                    book.read_date,
                    authorFilterText,
                    publisherFilterText,
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
        author_records: (a: AuthorView[], b: AuthorView[]) => {
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
    }

    onMounted(async () => {
        authors.value = await knockApi<AuthorView[]>("/api/author") ?? []
        publishers.value = await knockApi<PublisherView[]>("/api/publisher") ?? []
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

        <template #item.publisher="{ item }">
            <RouterLink :to="`/publisher/${item.publisher_id}`">
                {{ item.publisher }}
            </RouterLink>
        </template>
    </v-data-table>
</template>