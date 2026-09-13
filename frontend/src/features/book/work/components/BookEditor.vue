<script setup lang="ts">
    import type { BookEditRecord } from "@/types/book"

    const books = defineModel<BookEditRecord[]>({ required: true })

    function addItem() {
        books.value.push({
            id: null,
            title: null,
            volume: null,
            isbn: null,
            amazon_asin: null,
            registration_date: new Date().toLocaleDateString("sv-SE"),
            read_records: [],
        })
    }

    if (books.value.length === 0) {
        addItem()
    }

    function removeItem(index: number) {
        books.value.splice(index, 1)
    }

    function addReadRecord(item: BookEditRecord) {
        item.read_records.push({
            id: null,
            read_date: new Date().toLocaleDateString("sv-SE"),
        })
    }

    function removeReadRecord(item: BookEditRecord, index: number) {
        item.read_records.splice(index, 1)
    }

    const openNdl = async (isbn: string) => {
        const response = await fetch(
            `/api/ndl/${isbn}`
        )

        const json = await response.json()

        if (json) {
            window.open(json.link, "_blank")
        }
    }

    

</script>

<template>
    <v-btn
        prepend-icon="mdi-plus"
        variant="outlined"
        @click="addItem"
    >
    Add Book
    </v-btn>
<div
    v-for="(item, index) in books"
    :key="index"
    class="mb-2"
>
    <!-- 今までの入力フォーム -->
    <div class="d-flex align-center">
        <v-text-field
            v-model="item.title"
            label="サブタイトル"
            density="compact"
            hide-details
        />

        <v-text-field
            v-model="item.volume"
            label="巻数"
            density="compact"
            hide-details
        />

        <v-text-field
            v-model="item.isbn"
            label="ISBN"
            density="compact"
            hide-details
        />

        <v-btn 
            v-if="item.isbn" 
            icon="mdi-open-in-new"
            variant="text" 
            size="small" 
            @click="openNdl(item.isbn)" 
        />

        <v-text-field
            v-model="item.amazon_asin"
            label="Amazon ASIN"
            density="compact"
            hide-details
        />

        <v-btn
            v-if="item.amazon_asin"
            icon="mdi-open-in-new"
            variant="text"
            size="small"
            :href="`https://www.amazon.co.jp/dp/${item.amazon_asin}`"
            target="_blank"
            rel="noopener noreferrer"
        />

        <v-date-input
            v-model="item.registration_date"
            label="登録日"
            density="compact"
            hide-details
        />

        <v-btn
            icon="mdi-delete"
            variant="text"
            @click="removeItem(index)"
        />
    </div>

    <!-- 読了記録 -->
    <div class="ml-8 mt-1">
        <div
            v-for="(read, readIndex) in item.read_records"
            :key="read.id ?? readIndex"
            class="d-flex align-center"
        >
            <v-date-input
                v-model="read.read_date"
                label="読了日"
                density="compact"
                hide-details
            />

            <v-btn
                icon="mdi-delete"
                variant="text"
                size="small"
                @click="removeReadRecord(item, readIndex)"
            />
        </div>

        <v-btn
            prepend-icon="mdi-plus"
            variant="text"
            size="small"
            @click="addReadRecord(item)"
        >
            読了日を追加
        </v-btn>
    </div>
</div>
</template>