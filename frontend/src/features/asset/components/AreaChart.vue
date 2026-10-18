<script setup lang="ts">
    import { computed } from "vue"
    import type { AssetView } from "../types"
    import VChart from "vue-echarts"

    import { use } from 'echarts/core'
    import {
        LineChart
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
        LineSeriesOption
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
        LineChart,
        CanvasRenderer
    ])

    type EChartsOption = ComposeOption<
        | TooltipComponentOption
        | LegendComponentOption
        | GridComponentOption
        | LineSeriesOption
    >

    const props = defineProps<{
        assets: AssetView[]
    }>()

const option = computed<EChartsOption>(() => ({
  tooltip: {
    trigger: 'axis',
  },

  legend: {
    data: ['Cash', 'Fund', 'Pension', 'Stock'],
  },

  xAxis: {
    type: 'time',
  },

  yAxis: {
    type: 'value',
  },

  series: [
    {
      name: 'Cash',
      type: 'line',
      stack: 'asset',
      areaStyle: {},
      showSymbol: false,
      data: props.assets.map((asset) => [
        asset.date,
        asset.cash,
      ]),
    },
    {
      name: 'Fund',
      type: 'line',
      stack: 'asset',
      areaStyle: {},
      showSymbol: false,
      data: props.assets.map((asset) => [
        asset.date,
        asset.fund,
      ]),
    },
    {
      name: 'Pension',
      type: 'line',
      stack: 'asset',
      areaStyle: {},
      showSymbol: false,
      data: props.assets.map((asset) => [
        asset.date,
        asset.pension,
      ]),
    },
    {
      name: 'Stock',
      type: 'line',
      stack: 'asset',
      areaStyle: {},
      showSymbol: false,
      data: props.assets.map((asset) => [
        asset.date,
        asset.stock,
      ]),
    },
  ],
}))
</script>




<template>
    <VChart
        :option="option"
        style="width: 100%; height: 400px;"
    />
</template>