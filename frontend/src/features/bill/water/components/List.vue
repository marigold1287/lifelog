<script setup lang="ts">
import { BASE_URL } from "../router";
import { api } from "../api"
import BillListView from "../../components/List.vue"

</script>

<template>
    <BillListView
        :api="api"
        :base-url="BASE_URL"
    />
</template>