<script setup lang="ts">
import { computed, ref } from "vue"
import type { Response } from "../types"
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

type MetricKey = 'weight' | 'room_temperature' | 'room_humidity' | 'body_temperature'

const META: Record<MetricKey, { label: string; unit: string }> = {
  weight: { label: '体重', unit: 'kg' },
  room_temperature: { label: '室温', unit: '℃' },
  room_humidity: { label: '湿度', unit: '%' },
  body_temperature: { label: '体温', unit: '℃' },
}

// 選択肢（META のキー順）
const metricOptions = (Object.keys(META) as MetricKey[]).map(key => ({
  value: key,
  label: `${META[key].label} (${META[key].unit})`,
}))

const props = defineProps<{
  data: Response[]
}>()

const selected = ref<MetricKey>('weight')

const option = computed<EChartsOption>(() => generateOption(props.data, selected.value))

function generateOption(data: Response[], key: MetricKey): EChartsOption {
  const { label, unit } = META[key]
  return {
    tooltip: {
      trigger: 'axis',
      valueFormatter: (v) => `${v} ${unit}`,
    },
    xAxis: {
      type: 'time',
      axisLabel: { formatter: '{yyyy}/{MM}/{dd}' },
    },
    yAxis: {
      type: 'value',
      name: `${label} (${unit})`,
      scale: true,
      min: (value: { min: number }) => Math.floor(value.min - 1),
      max: (value: { max: number }) => Math.ceil(value.max + 1),
    },
    dataZoom: [{ type: 'inside' }, { type: 'slider' }],
    series: [
      {
        name: label,
        type: 'line',
        smooth: false,
        showSymbol: false,
        connectNulls: false,
        data: data.map(d => [d.date, d[key]]),
      },
    ],
  }
}
</script>

<template>
  <div>
    <select v-model="selected">
      <option v-for="m in metricOptions" :key="m.value" :value="m.value">
        {{ m.label }}
      </option>
    </select>

    <VChart
      :option="option"
      style="width: 100%; height: 400px;"
    />
  </div>
</template>