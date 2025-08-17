import { Component, OnInit } from '@angular/core';
import { ApiStockService } from '../services/api-stock.service';
import { ChartDataService } from '../services/chart-data.service';
import { predictionMetrics } from '../models/prediction-metrics';
import { TrackedStock } from '../models/tracked-stocks.interface';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-predicted-metrics',
  imports: [CommonModule],
  templateUrl: './predicted-metrics.component.html',
  styleUrl: './predicted-metrics.component.css'
})
export class PredictedMetricsComponent implements OnInit {
  private cardData: TrackedStock | null = null;
  private charTitle = '';
  stockPredictMetric: predictionMetrics | null = null;
  chatTitle = '';
  constructor(private chartDataService: ChartDataService, 
              private apiService: ApiStockService
  ){}
  ngOnInit(): void {
    this.chartDataService.chartData$.subscribe(data => {
      if (data){
        // console.log("chart update:", this.cardData);
        this.cardData = data;
        // Gneretaing array from the recived data
        this.charTitle = this.cardData.stock_title; 
        // console.log("chart data from mterics component:", this.cardData);
        this.loadPredictedMetrics(this.charTitle);
      }
      });
  }

  loadPredictedMetrics(stock:string){
    this.apiService.get_predicted_error(stock).subscribe(data => {
      this.stockPredictMetric = data;
      // console.log("chart data from predict mterics component:", this.stockPredictMetric);
    })
  }

}
