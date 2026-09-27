<script setup lang="ts">
import { onMounted, ref } from "vue"
import type { BookView } from "../types"
import { knockApi} from "@/api"
import BookList from "@/features/book/components/BookList.vue"

    const books = ref<BookView[]>([])

    onMounted(async () => {
        books.value = await knockApi<BookView[]>("/api/book")
    })
</script>


<template>
    <v-card
        title="Books"
        flat
    >

        <RouterLink :to="'/work/add'">
            <v-btn>Add New</v-btn>
        </RouterLink>

        <BookList
            :books="books"
        />

    </v-card>
</template>