import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { TrackedStock } from '../models/tracked-stocks.interface';
import { lstmPredictionInterface } from '../models/lstm-prediction';
@Injectable({
  providedIn: 'root'
})
export class ChartDataService {
  private chartDataSource = new BehaviorSubject<TrackedStock | null>(null);
  chartData$ = this.chartDataSource.asObservable();

  private lstmCartData = new BehaviorSubject<lstmPredictionInterface | null>(null);
  lstmCartData$ = this.lstmCartData.asObservable();

  constructor() { }
  updateChartData(data: TrackedStock) {
    this.chartDataSource.next(data);
  }

  updateLstmChart(lstmChartData: lstmPredictionInterface){
    this.lstmCartData.next(lstmChartData);
  }
}
