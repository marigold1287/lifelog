<script setup lang="ts">
import { onMounted, ref } from "vue"
import type { Publisher} from "@/types/book"
import { knockApi} from "@/api"
import { customFilter } from "@/features/book/publisher/scripts.ts"

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Name', key: 'name' },
  { title: 'よみがな', key: 'yomigana' },
]

const publishers = ref<Publisher[]>([])
const search = ref('')

onMounted(async () => {
  publishers.value = await knockApi<Publisher[]>("/api/publisher") ?? []
})

</script>


<template>
    <v-card
        title="Publisher"
        flat
    >

        <RouterLink :to="'/publisher/add'">
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
        :items="publishers"
        :custom-filter="customFilter"
        :search="search"
        >
            <template #item.id="{ item }">
                <RouterLink :to="`/publisher/${item.id}`">
                    {{ item.id }}
                </RouterLink>
            </template>
        </v-data-table>
    </v-card>
</template>