import { Injectable, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { apiUrls } from './api-urls';
import { TrackedStock } from '../models/tracked-stocks.interface';
import { trainingMetrics } from '../models/training_data';
import { Observable } from 'rxjs';
import { predictionMetrics } from '../models/prediction-metrics';
import { SentimentResult } from '../models/news-sentimental';
import { lstmPredictionInterface } from '../models/lstm-prediction';
import { isDevMode } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiStockService implements OnInit{
  private baseUrlApi : string = "http://stockapp.local/api";
  constructor(
    private httpClient: HttpClient
  ) { }

  ngOnInit(): void {
    if (isDevMode()){
      this.baseUrlApi = "http://localhost:5000";
    }
  }

  get_tracked_stocks(): Observable<TrackedStock[]> {
    return this.httpClient.get<TrackedStock[]>(this.baseUrlApi + apiUrls.get_tracked_stocks);
  }

  get_tracked_stock_training_metrics(stock: string): Observable<trainingMetrics> {
    return this.httpClient.get<trainingMetrics>(this.baseUrlApi + apiUrls.get_training_matrics + stock);
  }

  get_predicted_error(stock: string): Observable<predictionMetrics> {
    return this.httpClient.get<predictionMetrics>(this.baseUrlApi + apiUrls.get_predicted_metrics + stock);
  }

  getSentiments(stock: string): Observable<SentimentResult> {
    return this.httpClient.get<SentimentResult>(this.baseUrlApi + apiUrls.get_news_sentimental + stock);
  }

  getLstmPredictions(stock: string): Observable<lstmPredictionInterface>  {
    return this.httpClient.get<lstmPredictionInterface>(this.baseUrlApi + apiUrls.get_lstm_predictions + stock)
  }

}

