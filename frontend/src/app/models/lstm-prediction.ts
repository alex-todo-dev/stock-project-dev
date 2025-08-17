export interface lstmPredictionInterface{
    stock_title: string,
    next_five_day_predictions: lstmPoint[]
}

export interface lstmPoint{
    date: Date,
    price: number
}