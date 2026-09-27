<script setup lang="ts">

    import { onMounted, ref, computed, watch } from "vue"
    import { knockApi, CustomApiError } from "@/api"
    import type { PublisherView, LabelRecord } from "@/features/book/publisher/types"
    import { customFilter as customPublisherFilter } from "@/features/book/publisher/scripts.ts"
    import { validateStringEntered } from "@/validator"

    const publisher = defineModel<string>("publisher", { required: true }); 
    const publisherId = defineModel<number | null>("publisherId", { required: true }); 
    const label = defineModel<string>("label", { required: true }); 
    const labelId = defineModel<number | null>("labelId", { required: true }); 

    const publishers = ref<PublisherView[]>([])

    const labels = computed(() => {
        const publisher = publishers.value.find(
            p => p.id === publisherId.value
        )

        return publisher?.label_records ?? [{id: null, name: "レーベルなし"}]
    })

    function onPublisherChanged(value: PublisherView | string | null) {
        if (typeof value === "string") {
            value = publishers.value.find(p => p.name == value) ?? value
        }
        if (typeof value === "string") {
            publisher.value = value
            publisherId.value = null
        } else if (value === null) {
            publisher.value = ""
            publisherId.value = null
        } else {
            publisher.value = value.name
            publisherId.value = value.id
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
        () => publisher.value,
        (newPublisher, oldPublisher) => {
            if (oldPublisher === undefined) return

            if (newPublisher !== oldPublisher) {
                label.value = ""
            }
        }
    )


    onMounted(async () => {
        try {
            publishers.value = await knockApi<PublisherView[]>("/api/publisher") ?? [];
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
            v-if="publisherId"
            icon="mdi-open-in-new"
            variant="text"
            size="small"
            :href="`/publisher/${publisherId}`"
            target="_blank"
            rel="noopener noreferrer"
        />
        <v-combobox
            label="出版社"
            v-model="publisher"
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