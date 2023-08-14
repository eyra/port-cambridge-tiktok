import { Text } from './elements'

export type AggregationFunction = 'count' | 'mean' | 'sum' | 'count_pct' | 'pct'

export interface Axis {
  label?: string
  column: string
}

export interface AggregationGroup {
  label?: string
  column: string
  dateFormat?: DateFormat
}

export interface AggregationValue {
  label?: string
  column: string
  aggregate?: AggregationFunction
  group_by?: string
  secondAxis?: boolean
  z?: string
  zAggregate?: AggregationFunction
  addZeroes?: boolean
}

export interface ChartProps {
  title: Text
  group: AggregationGroup
  values: AggregationValue[]
  height?: number
}

export interface LineChartProps extends ChartProps {
  type: 'line'
}

export interface BarChartProps extends ChartProps {
  type: 'bar'
}

export interface AreaChartProps extends ChartProps {
  type: 'area'
}

export interface WordcloudProps extends ChartProps {
  type: 'wordcloud'
}

export type VisualizationType = LineChartProps | BarChartProps | AreaChartProps | WordcloudProps

export type AggregateRowIds = Record<string, string[]>

export type AggregatedData = Record<string, string | AggregateRowIds>[]

export interface AxisSettings {
  label: string
  secondAxis?: boolean
  tickerFormat?: TickerFormat
}

export type TickerFormat = 'percent' | 'default'

export interface VisualizationData {
  type: 'line' | 'bar' | 'area' | 'wordcloud'
  data: AggregatedData
  xKey: AxisSettings
  yKeys: Record<string, AxisSettings>
}

export type DateFormat =
  | 'auto'
  | 'year'
  | 'quarter'
  | 'month'
  | 'day'
  | 'hour'
  | 'month_cycle'
  | 'weekday_cycle'
  | 'day_cycle'
  | 'hour_cycle'
