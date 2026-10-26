<script setup lang="ts">
    import { onMounted, ref } from "vue"
    import type { View } from "../types.ts"
    import { getList } from "../api.ts"


    interface Result {
        success: string[]
        fail: string[]
    }

    const holdings = ref<View[]>([])
    const isFetchingPrices = ref<boolean>(false)
    const message = ref<string>("")


    
    const search = ref('')
    const headers = [
        { title: '名称', key: 'name' },
        { title: '銘柄種類', key: 'type' },
        { title: '総量', key: 'total_quantity' },
        { title: '取得コスト', key: 'acquisition_cost' },
        { title: '現在価値', key: 'current_value' },
        { title: '損益', key: 'profit_loss' },
        { title: '損益割合', key: 'profit_loss_rate' },
    ]

    const fetchPrices = async () => {
        isFetchingPrices.value = true

        try {
            const response = await fetch('/api/price/fetch', {
                method: 'POST',
            })

            if (!response.ok) {
                throw new Error('価格情報の取得に失敗しました')
            }

            const result: Result = await response.json()

            if (result.fail.length == 0 ) {
                message.value = "取得に成功しました"
            } else {
                message.value = `次の銘柄のデータ取得に失敗しました。${result.fail.join(", ")}。しばらく経ってから再試行してください`

            }
            

            // 必要なら取得後に銘柄一覧を再読み込みする
        } catch (error) {
            console.error(error)
        } finally {
            isFetchingPrices.value = false
        }
    }


    onMounted(async () => {
        holdings.value = await getList()
    })

</script>

<template>
    <v-card
        title="銘柄一覧"
        flat
    >

        <RouterLink :to="'/holding/add'">
        <v-btn>Add New</v-btn>
        </RouterLink>
        <v-btn
            color="primary"
            :loading="isFetchingPrices"
            :disabled="isFetchingPrices"
            @click="fetchPrices"
        >
            価格情報を取得
        </v-btn>
        <p v-if="message" style="color: greenyellow;">
            {{ message }}
        </p>
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
            :items="holdings"
            :search="search"
            :headers="headers"
        >
            <template #item.name="{ item }">
                <RouterLink :to="`holding/${item.id}`">
                    {{ item.name }}
                </RouterLink>
            </template>
        </v-data-table>
    </v-card>
</template>