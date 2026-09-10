export interface LabelRecord {
  id: number | null
  name: string
}

interface AliasRecord {
  id: number | null
  alias: string
}

export interface AuthorRecord {
  id: number
  name: string
  yomigana: string | null
  role: string | null
  alias_records: AliasRecord[]
}

export interface AuthorEditRecord {
  id: number | null
  name: string | null
  role: string | null
}

export interface WorkRecord {
  id: number
  author_records: AuthorRecord[]
  publisher_record: Publisher
  title: string
  // publisher: string
  // publisher_aliases: string[]
  // publisher_yomigana: string | null
  // publisher_id: number
  label: string
  label_id: number
}

export interface ReadDateRecord {
  id: number | null
  read_date: string
}

export interface BookEditRecord {
  id: number | null
  title: string | null
  volume: string | null
  isbn: string | null
  amazon_asin: string | null
  registration_date: string | null
  read_records: ReadDateRecord[]
}


export interface WorkEditRecord {
  author_records: AuthorEditRecord[]
  publisher_record: PublisherEdit
  book_records: BookEditRecord[]
  id: number | null
  title: string
  // publisher: string
  // publisher_id: number | null
  label: string
  label_id: number | null
}

export interface Publisher {
  id: number | null
  name: string
  yomigana: string
  label_records: LabelRecord[]
  alias_records: AliasRecord[]
}

export interface PublisherEdit {
  id: number | null
  name: string
}

export interface PublisherDetail extends Publisher {
  work_records: WorkRecord[]
}

export interface Author {
  id: number | null
  name: string
  yomigana: string
  alias_records: AliasRecord[]
  note: string
}

export interface AuthorDetail extends Author {
  work_records: WorkRecord[]
}

export interface Book {
  work_id: number
  author_records: AuthorRecord[]
  publisher_record: Publisher
  title: string
  label: string
  subtitle: string | null
  volume: string | null
  registration_date: Date
  read_date: Date | null
}