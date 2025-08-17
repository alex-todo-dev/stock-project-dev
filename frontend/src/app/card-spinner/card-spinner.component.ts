import { NgFor, NgForOf } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { StockDataCardComponent } from '../stock-data-card/stock-data-card.component';
import { ApiStockService } from '../services/api-stock.service';
import { TrackedStock } from '../models/tracked-stocks.interface';
import { ChartDataService } from '../services/chart-data.service';
import { HighlightDirective } from '../directives/highlight.directive';
import { lstmPredictionInterface } from '../models/lstm-prediction';
import { LstmPredictionDataService } from '../services/lstm-prediction-data.service';

@Component({
    selector: 'app-card-spinner',
    standalone: true,
    imports: [StockDataCardComponent, HighlightDirective],
    templateUrl: './card-spinner.component.html',
    styleUrl: './card-spinner.component.css'
})
export class CardSpinnerComponent implements OnInit{
  public trackedStocks: TrackedStock[] = [] ;
  constructor(
    private apiService: ApiStockService,
    private chartDataService: ChartDataService,
    private lstmPredictionDataService: LstmPredictionDataService) { }
  ngOnInit(): void {
    this.apiService.get_tracked_stocks().subscribe(
      {
        next: (response) => {
          this.trackedStocks = response;
        }
      });
    
  }
  chooseCard(card: TrackedStock) {
    console.log("Card:", card);
    this.chartDataService.updateChartData(card);
    // get lstm prediction data 
    this.apiService.getLstmPredictions(card.stock_title).subscribe( (data:lstmPredictionInterface) =>{
      this.lstmPredictionDataService.updateLstmChartData(data);
      console.log("Stock title lstm:",card.stock_title)
      console.log("stock lstm predictions:", data)
    });
  }
}
