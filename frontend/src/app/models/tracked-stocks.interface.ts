export interface TrackedStock {
    stock_title: string;
    first_buy_signal_data: Date;
    days_tracking: days_tracking[];
    next_day_predictions: next_day_predictions[];
    buy_signal: number;
}

interface  days_tracking{
    date: Date;
    closing_price: number;
    predicted_price: boolean;
}

interface next_day_predictions{
    date : Date;
    closing_price: number;
}