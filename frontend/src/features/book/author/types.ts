interface AliasRecord {
  id: number | null
  alias: string
}

export interface AuthorView {
    id: number
    name: string
    yomigana: string | null
    note: string | null
    alias_records: AliasRecord[]
}

export interface AuthorInput {
    name: string
    yomigana: string | null
    note: string | null
    alias_records: AliasRecord[]
}