import { Component,OnInit,Input} from '@angular/core';
import { ChartDataService } from '../services/chart-data.service';
import { TrackedStock } from '../models/tracked-stocks.interface';
import { ApiStockService } from '../services/api-stock.service';  
import { trainingMetrics } from '../models/training_data';
import { CommonModule } from '@angular/common';
@Component({
    selector: 'app-stock-details-metrics',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './stock-details-metrics.component.html',
    styleUrl: './stock-details-metrics.component.css'
})
export class StockDetailsMetricsComponent  implements OnInit{
  private cardData: TrackedStock | null = null;
  private charTitle = '';
  public stockMetric:trainingMetrics| null = null
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
        this.getTracketedStockMetric(this.charTitle);
      }
      });
  }

  getTracketedStockMetric(stock:string){
    this.apiService.get_tracked_stock_training_metrics(stock).subscribe(data => {
      this.stockMetric = data;
      console.log("chart data from mterics component:", this.stockMetric);
    })
  }
  
}