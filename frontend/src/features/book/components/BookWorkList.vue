<script setup lang="ts">
    import { ref, computed, onMounted } from "vue"
    import { knockApi } from "@/api";
    import type { PublisherView } from "@/features/book/publisher/types"
    import type { AuthorView } from "@/features/book/author/types"
    import type { WorkView } from "@/features/book/work/types"
    import { generateAuthorMap, generateSearchText } from "@/features/book/author/scripts";


    const props = defineProps<{
        works: WorkView[]
    }>()

    const authors = ref<AuthorView[]>([])
    const publishers = ref<PublisherView[]>([])

    const publisherMap = computed(() =>
        new Map(publishers.value.map(publisher => [publisher.id, publisher]))
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

    const headers = [
        { title: 'ID', key: 'id' },
        { title: 'Title', key: 'title' },
        { title: 'Authors', key: 'author_records' },
        { title: 'Publisher', key: 'publisher' },
        { title: 'Label', key: 'label' },
    ]

    const search = ref('')

    const worksForTable = computed(() =>
        props.works.map(work => {
            const publisher = publisherMap.value.get(work.publisher_id)
            const label = labelMap.value.get(work.label_id)

            const bookAuthors = work.author_ids
                .map(id => authorMap.value.get(id))
                .filter((author): author is AuthorView => author != null)

            const authorFilterText = bookAuthors
                .map(author => generateSearchText(author))
                .join(" ")

            return {
                ...work,
                publisher_id: publisher?.id,
                publisher: publisher?.name,
                author_records: bookAuthors,
                label: label?.name,
                _searchText: [
                    work.title,
                    work.yomigana,
                    authorFilterText,
                    publisher?.name,
                    publisher?.yomigana,
                    ...(publisher?.alias_records ?? []).map(record => record.alias),
                    label?.name,
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
        :items="worksForTable"
        :search="search"
        :custom-key-sort="customKeySort"
        :sort-by="[{ key: 'id', order: 'desc' }]"
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

        <template #item.publisher="{ item }">
            <RouterLink :to="`/publisher/${item.publisher_id}`">
                {{ item.publisher }}
            </RouterLink>
        </template>
    </v-data-table>
</template>