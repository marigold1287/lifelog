<script setup lang="ts">

    import { onMounted, ref, computed, watch } from "vue"
    import type { Publisher, PublisherEdit, LabelRecord } from "@/types/book"
    import { knockApi, CustomApiError } from "@/api"
    import { customFilter as customPublisherFilter } from "@/features/book/publisher/scripts.ts"
    import { validateStringEntered } from "@/validator"

    const publisherRecord = defineModel<PublisherEdit>("publisher", { required: true }); 
    const labelId = defineModel<number | null>("labelId", { required: true }); 
    const label = defineModel<string>("label", { required: true }); 

    const publishers = ref<Publisher[]>([])

    const labels = computed(() => {
        const publisher = publishers.value.find(
            p => p.id === publisherRecord.value.id
        )

        return publisher?.label_records ?? [{id: null, name: "レーベルなし"}]
    })

    function onPublisherChanged(value: Publisher | string | null) {
        if (typeof value === "string") {
            value = publishers.value.find(p => p.name == value) ?? value
        }
        if (typeof value === "string") {
            publisherRecord.value.name = value
            publisherRecord.value.id = null
        } else if (value === null) {
            publisherRecord.value.name = ""
            publisherRecord.value.id = null
        } else {
            publisherRecord.value.name = value.name
            publisherRecord.value.id = value.id
        }
    }

    function onLabelChanged(value: LabelRecord | string | null) {
        if (typeof value === "string") {
            value = labels.value.find(l => l.name == value) ?? value
        }
        if (typeof value === "string") {
            label.value = value
            labelId.value = null
        } else if (value === null) {
            label.value = ""
            labelId.value = null
        } else {
            label.value = value.name
            labelId.value = value.id
        }
    }

    watch(
        () => publisherRecord.value.name,
        (newPublisher, oldPublisher) => {
            if (oldPublisher === undefined) return

            if (newPublisher !== oldPublisher) {
                label.value = ""
            }
        }
    )


    onMounted(async () => {
        try {
            publishers.value = await knockApi<Publisher[]>("/api/publisher") ?? [];
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
    <div
        class="d-flex align-center mb-2"
    >
        <v-btn
            v-if="publisherRecord.id"
            icon="mdi-open-in-new"
            variant="text"
            size="small"
            :href="`/publisher/${publisherRecord.id}`"
            target="_blank"
            rel="noopener noreferrer"
        />
        <v-combobox
            label="出版社"
            v-model="publisherRecord.name"
            :items="publishers"
            item-title="name"
            item-value="name"
            :custom-filter="customPublisherFilter"
            :rules="[validateStringEntered]"
            @update:model-value="onPublisherChanged"
        />
    </div>

    <v-combobox
        label="レーベル"
        v-model="label"
        :items="labels"
        item-title="name"
        item-value="name"
        :rules="[validateStringEntered]"
        @update:model-value="onLabelChanged"
    />
</template>