<script setup lang="ts">
import { onMounted, ref } from "vue"
import type { Book } from "@/types/book"
import { knockApi} from "@/api"
import BookList from "@/components/BookList.vue"

    const books = ref<Book[]>([])

    async function fetchBooks() {
        const data = await knockApi("/api/book")
        return data;
    }

    onMounted(async () => {
        books.value = await fetchBooks()
        console.log(books)
    })

</script>


<template>
    <v-card
        title="Works"
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