export interface chartDataLine{
    name: string,
    series: chartPoint[]
}

export interface chartPoint{
    name: Date,
    value: number
}