<script setup lang="ts">
defineProps<{
    label: string
}>()

const model = defineModel<number>({
    required: true,
})
</script>

<template>
    <div class="compact-input-form">
        <label>{{ label }}</label>

        <v-number-input
            v-model="model"
            hide-details
            density="compact"
        />
    </div>
</template>

<style scoped>
.compact-input-form {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 8px;
}

.compact-input-form label {
    width: 120px;
}
</style>
