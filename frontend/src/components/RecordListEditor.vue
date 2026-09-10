<script setup lang="ts" generic="T extends Record<string, any>">
    const items = defineModel<T[]>({ required: true })

    const props = withDefaults(defineProps<{
        label?: string
        addLabel?: string
        itemKey?: string
    }>(), {
        label: "Data",
        addLabel: "Add New Data",
        itemKey: "value",
    })

    if (items.value.length === 0) {
        addItem()
    }

    function addItem() {
        const newItem = {
            id: null,
            [props.itemKey]: ""
        } as unknown as T
        items.value.push(newItem)
    }

    function removeItem(index: number) {
        items.value.splice(index, 1)
    }
</script>

<template>
  <div>
    <v-btn
      prepend-icon="mdi-plus"
      variant="outlined"
      @click="addItem"
    >
      {{ addLabel }}
    </v-btn>

    <div
      v-for="(item, index) in items"
      :key="index"
      class="d-flex align-center mb-2"
    >
      <v-text-field
        v-model="item[itemKey as keyof T]"
        :label="label"
        density="compact"
        hide-details
      />

      <v-btn
        icon="mdi-delete"
        variant="text"
        @click="removeItem(index)"
      />
    </div>
  </div>
</template>