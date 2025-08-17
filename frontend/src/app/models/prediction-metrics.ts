export interface predictionMetrics {
    stock_title: string
    prediction_error: {
        MAE: number,
        MSE: number,
        RMSE: number
    }
    trend: {
        status: string,
        delta: number,
        precentage_delta: number
    }
    sell_signal:{
        date: string,
        sell_signal: boolean,
        close_price: number,
        rsi: number,
        ma20: number
    }

}