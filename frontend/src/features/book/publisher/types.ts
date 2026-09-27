interface AliasRecord {
  id: number | null
  alias: string
}

export interface LabelRecord {
    id: number | null
    name: string
}

export interface PublisherView {
    id: number
    name: string
    yomigana: string | null
    alias_records: AliasRecord[]
    label_records: LabelRecord[]
}

export interface PublisherInput {
    name: string
    yomigana: string | null
    alias_records: AliasRecord[]
    label_records: LabelRecord[]
}