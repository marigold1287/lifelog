export interface Response {
    id: number
    date: string
    weight: number | null
    room_temperature: number | null
    room_humidity: number | null
    body_temperature: number | null
}

export interface Input {
    date: string
    weight: number | null
    room_temperature: number | null
    room_humidity: number | null
    body_temperature: number | null
}


export interface Draft {
    date: Date | null
    weight: number | null
    room_temperature: number | null
    room_humidity: number | null
    body_temperature: number | null
}
