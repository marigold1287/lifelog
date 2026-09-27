export interface BookView {
  work_id: number
  author_ids: number[]
  publisher_id: number
  label_id: number
  title: string
  yomigana: string | null
  subtitle: string | null
  volume: string | null
  registration_date: string
  read_date: string | null
}

export interface ReadDateInput {
    id: number | null
    read_date: Date
}

export interface BookInput {
    id: number | null
    title: string | null
    volume: string | null
    isbn: string | null
    amazon_asin: string | null
    registration_date: Date
    read_dates: ReadDateInput[]
}

export interface BookResponse {
    id: number | null
    title: string | null
    volume: string | null
    isbn: string | null
    amazon_asin: string | null
    registration_date: string
    read_dates: ReadDateResponse[]
}

export interface ReadDateResponse {
    id: number | null
    read_date: string
}