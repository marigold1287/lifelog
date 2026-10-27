<script setup lang="ts">
import { computed, ref } from "vue"
import type { PriceInput } from "../types"
import VChart from "vue-echarts"

import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import {
  TooltipComponent,
  GridComponent,
  DataZoomComponent,
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import type { ComposeOption } from 'echarts/core'
import type { LineSeriesOption } from 'echarts/charts'
import type {
  TooltipComponentOption,
  GridComponentOption,
  DataZoomComponentOption,
} from 'echarts/components'

use([
  TooltipComponent,
  GridComponent,
  DataZoomComponent,
  LineChart,
  CanvasRenderer,
])

type EChartsOption = ComposeOption<
  | TooltipComponentOption
  | GridComponentOption
  | DataZoomComponentOption
  | LineSeriesOption
>

const props = defineProps<{
  data: PriceInput[]
}>()

const option = computed<EChartsOption>(() => generateOption(props.data))

function generateOption(data: PriceInput[],): EChartsOption {
  return {
    tooltip: {
      trigger: 'axis',
    },
    xAxis: {
      type: 'time',
      axisLabel: { formatter: '{yy}/{MM}' },
    },
    yAxis: {
      type: 'value',
      name: `株価/基準価額`,
      scale: true,
      min: 0,
    },
    dataZoom: [{ type: 'inside' }, { type: 'slider' }],
    series: [
      {
        name: "価格",
        type: 'line',
        smooth: false,
        showSymbol: false,
        connectNulls: false,
        data: data.map(d => [d.price_date, d.price]),
      },
    ],
  }
}
</script>

<template>
  <div>
    <VChart
      :option="option"
      style="width: 100%; height: 400px;"
    />
  </div>
</template>