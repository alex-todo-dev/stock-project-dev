def trend_calculation(stock):
    status = ''
    print("Calaculating trend for stock")
    flagging_date_price = stock.get('days_tracking')[0].get('closing_price')
    today_price = stock.get('days_tracking')[-1].get('closing_price')

    print("Flagging date price:", flagging_date_price)
    print("Today price:", today_price)
    if (flagging_date_price < today_price):
        status = 'up'
    elif (flagging_date_price > today_price):
        status = 'down'
    else:
        status = 'no data'
    # calculate delta in precentage 
    precentage_delta = ((today_price - flagging_date_price) / flagging_date_price) * 100
    return {'status': status, 'delta': today_price - flagging_date_price, 'precentage_delta': precentage_delta}
