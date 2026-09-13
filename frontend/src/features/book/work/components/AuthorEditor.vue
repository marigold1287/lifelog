<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import type { Author, AuthorEditRecord } from "@/types/book"
    import { knockApi, CustomApiError } from "@/api"
    import { customFilter as customAuthorFilter } from "@/features/book/author/scripts.ts"
    import { validateStringEntered } from "@/validator"

    const authors = ref<Author[]>([])

    const items = defineModel<AuthorEditRecord[]>({ required: true })

    if (items.value.length === 0) {
        addItem()
    }

    function onAuthorChanged(item: AuthorEditRecord, author: Author | string) {
        if (typeof author === "string") {
            author = authors.value.find(a => a.name == author) ?? author
        }
        if (typeof author === "string") {
            item.name = author
            item.id = null
        } else if (author === null) {
            item.name = ""
            item.id = null
        }  else {
            item.name = author.name
            item.id = author.id
        }
    }

    function addItem() {
        items.value.push({
            id: null,
            name: null,
            role: null
        })
    }

    function removeItem(index: number) {
        items.value.splice(index, 1)
    }

    onMounted(async () => {
        try {
            authors.value = await knockApi<Author[]>("/api/author") ?? [];
        } catch (error) {
            if (error instanceof CustomApiError) {
                alert(error.message);
            } else {
                alert("データの取得に失敗しました");
            }
        }
    })
</script>

<template>
    <v-btn
        prepend-icon="mdi-plus"
        variant="outlined"
        @click="addItem"
    >
    Add Author
    </v-btn>
    <div
        v-for="(item, index) in items"
        :key="index"
        class="d-flex align-center mb-2"
    >
        <v-btn
            v-if="item.id"
            icon="mdi-open-in-new"
            variant="text"
            size="small"
            :href="`/author/${item.id}`"
            target="_blank"
            rel="noopener noreferrer"
        />
        <v-combobox
            v-model="item.name"
            :items="authors"
            label="著者名"
            item-title="name"
            item-value="name"
            :rules="[validateStringEntered]"
            density="compact"
            :custom-filter="customAuthorFilter"
            @update:model-value="onAuthorChanged(item, $event)"
            hide-details
        />
        <v-text-field
            v-model="item.role"
            label="役割"
            density="compact"
            hide-details
        />

        <v-btn
            icon="mdi-delete"
            variant="text"
            @click="removeItem(index)"
        />
    </div>
</template>