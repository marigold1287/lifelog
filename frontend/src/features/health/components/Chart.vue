<script setup lang="ts">
import { computed } from "vue"
import VChart from "vue-echarts"
import type { Response, MetricKey } from "../types"

import { use } from 'echarts/core'
import {
    LineChart
} from 'echarts/charts'
import {
    TooltipComponent,
    GridComponent,
    DataZoomComponent,
    MarkLineComponent
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
    GridComponentOption,
    DataZoomComponentOption,
    MarkLineComponentOption
} from 'echarts/components'

use([
    TooltipComponent,
    GridComponent,
    DataZoomComponent,
    MarkLineComponent,
    LineChart,
    CanvasRenderer
])

type EChartsOption = ComposeOption<
    | TooltipComponentOption
    | GridComponentOption
    | DataZoomComponentOption
    | MarkLineComponentOption
    | LineSeriesOption
>

type Point = [string, number | null]



const props = withDefaults(
  defineProps<{
    yAxisLabel: string,
    health: Response[],
    data_name: MetricKey,
    upperLimit?: number | null
    lowerLimit?: number | null
  }>(),
  {
    upperLimit: null,
    lowerLimit: null,
  },
)

const option = computed<EChartsOption>(() => {
  
  console.log(generateOption(
    props.health,
    props.yAxisLabel,
    props.data_name,
    props.upperLimit,
    props.lowerLimit
  ))
  
  return generateOption(
    props.health,
    props.yAxisLabel,
    props.data_name,
    props.upperLimit,
    props.lowerLimit
  )
})

function generateOption(
  health: Response[],
  yLabel: string, 
  data_name: MetricKey,
  upperLimit: number | null,
  lowerLimit: number | null,
): EChartsOption {
  console.log(yLabel)
  console.log(health)
  const sortedHealth = [...health].sort((a, b) => a.date.localeCompare(b.date));
  const data = sortedHealth.map(h => [h.date, h[data_name]])
  const series: LineSeriesOption[] = [
    {
        name: yLabel,
        type: 'line',
        smooth: false,
        showSymbol: false,
        connectNulls: false,
        data: data,
    },
  ]

  const markLineData: { yAxis: number; name: string }[] = []
  if (upperLimit != null) markLineData.push({ yAxis: upperLimit, name: '上限' })
  if (lowerLimit != null) markLineData.push({ yAxis: lowerLimit, name: '下限' })

  // 修正: markLineData が存在する場合のみ設定し、ハードコードを修正
  if (markLineData.length > 0) {
    if (series[0] === undefined) {
      throw new Error("Can't access Series[0]")
    } 
    series[0].markLine = {
      silent: true,
      symbol: ['none', 'none'],
      lineStyle: {
        color: '#f44336',
        type: 'dashed',
        width: 2,
      },
      data: markLineData, // ← ここを修正（準備した配列を渡す）
    }
  }

  const yMin = Math.min(
    ...[lowerLimit, ...data.map(d => d[1])].filter(v => v != null && typeof v == "number")
  );
  const yMax = Math.max(
    ...[upperLimit, ...data.map(d => d[1])].filter(v => v != null && typeof v == "number")
  );

  return {
    tooltip: {
      trigger: 'axis',
    },
    xAxis: {
      type: 'time',
      axisLabel: { formatter: '{yyyy}/{MM}/{dd}' },
    },
    yAxis: {
      type: 'value',
      name: yLabel,
      scale: true,
      min: yMin - 1,
      max: yMax + 1,
    },
    series: series,
  }
}
</script>

<template>
    <VChart :option="option" style="height: 400px; width: 100%;" autoresize />
</template>