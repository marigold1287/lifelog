<script setup lang="ts">
    import { computed, ref } from "vue"
    import type { View } from "../types"
    import VChart from "vue-echarts"
    import { groupPayslipsByYearMonth } from "../utils"

    import { use } from 'echarts/core'
    import {
        BarChart
    } from 'echarts/charts'
    import {
        TooltipComponent,
        LegendComponent,
        GridComponent
    } from 'echarts/components'
    import {
        CanvasRenderer
    } from 'echarts/renderers'
    import type { ComposeOption } from 'echarts/core'
    import type {
        BarSeriesOption
    } from 'echarts/charts'
    import type {
        TooltipComponentOption,
        LegendComponentOption,
        GridComponentOption
    } from 'echarts/components'

    use([
        TooltipComponent,
        LegendComponent,
        GridComponent,
        BarChart,
        CanvasRenderer
    ])

    type EChartsOption = ComposeOption<
        | TooltipComponentOption
        | LegendComponentOption
        | GridComponentOption
        | BarSeriesOption
    >


    const props = defineProps<{
        payslips: View[]
    }>()

    const option = computed(() => {
        return generateOption(props.payslips)
    })

    const selected = ref<Record<string, boolean>>({})

    const onLegendSelectChanged = (params: any) => {
        selected.value = params.selected
    }

    function generateOption(payslips: View[]) {
        const { years, months: sortedMonths, grouped } = groupPayslipsByYearMonth(payslips)

        const totals = years.map(year =>
            sortedMonths.reduce((sum, month) => {
                const name = `${month + 1}月`

                if (selected.value[name] === false) {
                    return sum
                }

                return sum + (grouped[year]?.[month] ?? 0)
            }, 0)
        )

        const series = [
            ...sortedMonths.map(month => ({
                name: `${month + 1}月`,
                type: "bar",
                stack: "total",
                data: years.map(year => grouped[year]?.[month] ?? 0),
            })),

            // 合計ラベル表示用の透明シリーズ
            {
                name: "total",
                type: "bar",
                stack: "total",
                data: years.map(() => 0),
                itemStyle: { color: "transparent" },
                tooltip: { show: false },
                label: {
                    show: true,
                    position: "top",
                    formatter: (params: any) => totals[params.dataIndex]?.toLocaleString(),
                    color: "#ffffff",
                },
            },
        ]

        return {
            tooltip: {
                trigger: "axis"
            },

            legend: {
                data: sortedMonths.map(month => `${month + 1}月`),
                textStyle: {
                    color: '#ffffff',
                },
            },

            xAxis: {
                type: "category",
                data: years,
                axisLabel: {
                    color: '#ffffff',
                },
                axisLine: {
                    lineStyle: {
                        color: '#ffffff',
                    },
                },
                axisTick: {
                    lineStyle: {
                        color: '#ffffff',
                    },
                },
            },

            yAxis: {
                type: "value",
                name: "手取り",
                axisLabel: {
                    color: '#ffffff',
                },
                axisLine: {
                    lineStyle: {
                        color: '#ffffff',
                    },
                },
                axisTick: {
                    lineStyle: {
                        color: '#ffffff',
                    },
                },
            },

            series
        }
    }
</script>




<template>
    <VChart
        :option="option"
        @legendselectchanged="onLegendSelectChanged"
        style="width: 100%; height: 400px;"
    />
</template>