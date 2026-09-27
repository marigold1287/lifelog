<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import type { WorkView } from "@/features/book/work/types"
    import { knockApi} from "@/api"
    import BookWorkList from "@/features/book/components/BookWorkList.vue"

    const works = ref<WorkView[]>([])

    onMounted(async () => {
        works.value = await knockApi<WorkView[]>("/api/work")
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