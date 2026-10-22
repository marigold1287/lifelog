<script setup lang="ts">
    import type { BookInput } from "@/features/book/book/types"
    import { knockApi, CustomApiError } from "@/api"

    const books = defineModel<BookInput[]>({ required: true })

    type Response = {
        link: string
        ndlbib: string | null
    }

    function addItem() {
        books.value.push({
            id: null,
            title: null,
            volume: null,
            isbn: null,
            ndlbib: null,
            amazon_asin: null,
            registration_date: new Date(),
            read_dates: [],
        })
    }

    if (books.value.length === 0) {
        addItem()
    }

    function removeItem(index: number) {
        books.value.splice(index, 1)
    }

    function addReadRecord(item: BookInput) {
        item.read_dates.push({
            id: null,
            read_date: new Date(),
        })
    }

    function removeReadRecord(item: BookInput, index: number) {
        item.read_dates.splice(index, 1)
    }

    const searchNdlBib = async (index: number, isbn: string) => {
        try {
            const normalizedIsbn = isbn.replace(/[-\s]/g, "")
            const data = await knockApi<Response>(
                `/api/ndl/${normalizedIsbn}`
            )

            if (data && data.ndlbib !== null && books.value[index] !== undefined) {
                books.value[index].ndlbib = data.ndlbib
            }
        } catch(error) {
            if (error instanceof CustomApiError) {
                alert(error.message)
            } else {
                alert("リンクの取得に失敗しました")
            }
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
            v-model="item.ndlbib"
            label="NDLBib"
            density="compact"
            hide-details
        />

        <v-btn 
            v-if="item.ndlbib" 
            icon="mdi-open-in-new"
            variant="text"
            size="small"
            :href="`https://ndlsearch.ndl.go.jp/books/R100000002-I${item.ndlbib}`"
            target="_blank"
        />

        <v-text-field
            v-model="item.isbn"
            label="ISBN"
            density="compact"
            hide-details
        />

        <v-tooltip text="NDLサーチで書誌情報を検索" location="top">
        <template #activator="{ props }">
            <v-btn
            v-if="item.isbn"
            v-bind="props"
            icon="mdi-book-search-outline"
            variant="text"
            size="small"
            @click="searchNdlBib(index, item.isbn)"
            />
        </template>
        </v-tooltip>

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
            v-for="(read, readIndex) in item.read_dates"
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