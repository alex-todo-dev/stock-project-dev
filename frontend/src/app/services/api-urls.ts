export const apiUrls = {
    base_url : "http://localhost:5000",
    base_url_kube : "http://flask-service.stockapp.svc.cluster.local:5000", 
    base_url_url: "http://stockapp.local",
    get_tracked_stocks: "/buy-signal-all-stocks",
    get_training_matrics: "/training-data/",
    get_predicted_metrics: "/result-data/",
    get_news_sentimental: "/stock-sentiment/",
    get_lstm_predictions: "/lstm-predictions/"
   }