import type { BookInput, BookResponse } from "@/features/book/book/types"

export interface WorkView {
    id: number
    title: string
    yomigana: string | null
    publisher_id: number
    label_id: number
    author_ids: number[]
}

export interface AuthorInput {
    id: number | null
    name: string
    role: string | null
}

export interface WorkInput {
    title: string
    yomigana: string | null
    publisher: string
    publisher_id: number | null
    label: string
    label_id: number | null
    author_records: AuthorInput[]
    book_records: BookInput[]
}


export interface WorkResponse {
    title: string
    yomigana: string | null
    publisher: string
    publisher_id: number | null
    label: string
    label_id: number | null
    author_records: AuthorInput[]
    book_records: BookResponse[]
}