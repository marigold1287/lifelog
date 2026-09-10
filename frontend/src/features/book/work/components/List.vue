<script setup lang="ts">
import { onMounted, ref } from "vue"
import type { WorkRecord } from "@/types/book"
import { knockApi} from "@/api"
import BookWorkList from "@/components/BookWorkList.vue"

    const works = ref<WorkRecord[]>([])

    async function fetchWorks() {
        const data = await knockApi("/api/work")
        return data;
    }

    onMounted(async () => {
    works.value = await fetchWorks()
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

        <BookWorkList
            :works="works"
        />

    </v-card>
</template>