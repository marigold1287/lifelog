<script setup lang="ts">
import { onMounted, ref } from "vue"
import type { Response, MetricKey } from "../types"
import { getList } from "../api"
import Chart from "./Chart.vue"

const headers = [
  { title: 'Date', key: 'date' },
  { title: '胸囲', key: 'waist' },
  { title: 'BMI', key: 'bmi' },
  { title: '最高血圧', key: 'systolic_bp' },
  { title: '最低血圧', key: 'diastolic_bp' },
  { title: '血糖値', key: 'blood_glucose' },
  { title: 'HbA1c', key: 'hba1c' },
  { title: 'HDL', key: 'hdl_cholesterol' },
  { title: 'LDL', key: 'ldl_cholesterol' },
  { title: '中性脂肪', key: 'triglycerides' },
  { title: 'AST', key: 'ast' },
  { title: 'ALT', key: 'alt' },
  { title: 'γ-GTP', key: 'gamma_gtp' },
]

const health = ref<Response[]>([])
const search = ref('')


type Point = [string, number | null]


const rows = ref<Response[]>([])
const labels = ref<string[]>([])
const systolic_bp = ref<Point[]>([])
const diastolic_bp = ref<Point[]>([])

onMounted(async () => {
    health.value = await getList()
})
</script>


<template>
    <v-card
        title="健康診断"
        flat
    >

        <RouterLink :to="'/health/add'">
        <v-btn>Add New</v-btn>
        </RouterLink>
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
        :items="health"
        :search="search"
        :headers="headers"
        :sort-by="[{ key: 'date', order: 'desc' }]"
        >
            <template #item.date="{ item }">
                <RouterLink :to="`/health/${item.id}`">
                    {{ item.date }}
                </RouterLink>
            </template>
        </v-data-table>
    </v-card>
    <h1>血圧</h1>
    <v-row>
        <v-col cols="12" md="6">
            <Chart
            y-axis-label="最高血圧"
            :health="health"
            data_name="systolic_bp"
            :upper-limit="130"
            :lower-limit="null"
            />
        </v-col>
        <v-col cols="12" md="6">
            <Chart
            y-axis-label="最低血圧"
            :health="health"
            data_name="diastolic_bp"
            :upper-limit="84"
            :lower-limit="null"
            />
        </v-col>
    </v-row>
    <h1>身体計測</h1>
    <v-row>
        <v-col cols="12" md="6">
            <Chart
                y-axis-label="BMI"
                :health="health"
                data_name="bmi"
                :upper-limit="24.9"
                :lower-limit="18.5"
            />
        </v-col>
        <v-col cols="12" md="6">
            <Chart
                y-axis-label="胸囲, cm"
                :health="health"
                data_name="waist"
                :upper-limit="84.9"
                :lower-limit="null"
            />
        </v-col>
    </v-row>
    <h1>脂質</h1>
    <v-row>
        <v-col cols="12" md="4">
            <Chart
                y-axis-label="HDL (mg/dL)"
                :health="health"
                data_name="hdl_cholesterol"
                :upper-limit="null"
                :lower-limit="40"
            />
        </v-col>
        <v-col cols="12" md="4">
            <Chart
                y-axis-label="LDL (mg/dL)"
                :health="health"
                data_name="ldl_cholesterol"
                :upper-limit="119"
                :lower-limit="60"
            />
        </v-col>
        <v-col cols="12" md="4">
            <Chart
                y-axis-label="中性脂肪 (mg/dL)"
                :health="health"
                data_name="triglycerides"
                :upper-limit="149"
                :lower-limit="30"
            />
        </v-col>
    </v-row>
    <h1>糖代謝</h1>
    <v-row>
        <v-col cols="12" md="6">
            <Chart
                y-axis-label="血糖 (mg/dL)"
                :health="health"
                data_name="blood_glucose"
                :upper-limit="99"
                :lower-limit="null"
            />
        </v-col>
        <v-col cols="12" md="6">
            <Chart
                y-axis-label="HbA1c (%)"
                :health="health"
                data_name="hba1c"
                :upper-limit="5.5"
                :lower-limit="null"
            />
        </v-col>
    </v-row>
    <h1>肝機能</h1>
    <v-row>
        <v-col cols="12" md="4">
            <Chart
                y-axis-label="AST (U/L)"
                :health="health"
                data_name="ast"
                :upper-limit="30"
                :lower-limit="10"
            />
        </v-col>
        <v-col cols="12" md="4">
            <Chart
                y-axis-label="ALT (U/L)"
                :health="health"
                data_name="alt"
                :upper-limit="30"
                :lower-limit="5"
            />
        </v-col>
        <v-col cols="12" md="4">
            <Chart
                y-axis-label="γ-GTP (U/L)"
                :health="health"
                data_name="gamma_gtp"
                :upper-limit="50"
                :lower-limit="0"
            />
        </v-col>
    </v-row>
</template>