<script setup lang="ts">
    import { api } from "../api"
    import { BASE_URL } from "../router"
    import DetailView from "@/features/bill/components/Detail.vue"
</script>

<template>
    <DetailView 
        :api="api"
        :base-url="BASE_URL"
    />

</template>