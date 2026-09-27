<script setup lang="ts">
    import { api } from "../api"
    import { BASE_URL } from "../router"
    import AddView from "@/features/bill/components/Add.vue"
</script>

<template>
    <AddView 
        :api="api"
        :base-url="BASE_URL"
        provider="東京水道局"
    />

</template>