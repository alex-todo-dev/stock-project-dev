import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { lstmPredictionInterface } from '../models/lstm-prediction';
@Injectable({
  providedIn: 'root'
})
export class LstmPredictionDataService {
    private chartDataSource = new BehaviorSubject<lstmPredictionInterface | null>(null);
  chartData$ = this.chartDataSource.asObservable();

  constructor() { }
  updateLstmChartData(data: lstmPredictionInterface) {
    this.chartDataSource.next(data);
  }
  
}


