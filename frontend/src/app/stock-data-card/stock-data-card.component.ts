import { Component,Input, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common'; 
import { ApiStockService } from '../services/api-stock.service';
import { trainingMetrics } from '../models/training_data';
import { predictionMetrics } from '../models/prediction-metrics';
import { CommonModule } from '@angular/common';
import { CapitalizePipe } from '../capitalize.pipe';
import { MatTooltipModule} from '@angular/material/tooltip';
import { TooltipPosition} from '@angular/material/tooltip';
import { FormControl, FormsModule, ReactiveFormsModule} from '@angular/forms';
import { SentimentResult} from '../models/news-sentimental';
@Component({
    selector: 'app-stock-data-card',
    standalone: true,
    imports: [DatePipe, CommonModule, CapitalizePipe, MatTooltipModule],
    templateUrl: './stock-data-card.component.html',
    styleUrl: './stock-data-card.component.css'
})
export class StockDataCardComponent implements OnInit{
  public selectedCardIndex: number | null = null;
  public stockMetric:trainingMetrics | null = null;
  public stockPredictMetric:predictionMetrics | null = null;
  public sentiment: SentimentResult | null = null;
  ngOnInit(): void {
    this.apiService.getSentiments(this.stockTitle).subscribe(data => {
      this.sentiment = data;
      // console.log("sentiment data for stock:" + this.stockTitle, this.sentiment);
    });

    this.apiService.get_predicted_error(this.stockTitle).subscribe(data => {
      this.stockPredictMetric = data;
      // console.log("chart data from predict mterics component:", this.stockPredictMetric);
    });

    this.apiService.get_tracked_stock_training_metrics(this.stockTitle).subscribe(data => {
      this.stockMetric = data;
      // console.log("mteric", this.stockMetric)
    });

    this.apiService.getLstmPredictions(this.stockTitle).subscribe(data=>{
      // console.log("Stoct LSTM 5 days prediction")
      // console.log(data)
    });
  }
  constructor(private apiService: ApiStockService) { 

  }
  @Input() stockTitle: string = 'Stock Title';
  @Input() buyFlagDate: Date = new Date();
  @Input() priceAtFlag: number = 0;
  @Input() nextDayPrediction: number = 0;
  @Input() buyFlagValue: number = 0;

  positionOptions: TooltipPosition[] = ['after', 'before', 'above', 'below', 'left', 'right'];
  position = new FormControl(this.positionOptions[0]);
  selectCard(index: number): void {
    this.selectedCardIndex = index;
  }

  getSentimentColor(polarity: number | undefined): string {
    if (polarity === undefined) return '#cccccc'; // fallback
    if (polarity > 0.05) {
      return this.interpolateColor('#FFFF00', '#00FF00', polarity); // Yellow → Green
    } else if (polarity < -0.05) {
      return this.interpolateColor('#FFFF00', '#FF0000', -polarity); // Yellow → Red
    } else {
      return '#FFFF00'; // Neutral
    }
  }
  
  // Utility to interpolate between two hex colors
  interpolateColor(color1: string, color2: string, t: number): string {
    const hexToRgb = (hex: string) =>
      hex.match(/\w\w/g)?.map(x => parseInt(x, 16)) ?? [0, 0, 0];
  
    const rgbToHex = (r: number, g: number, b: number) =>
      '#' + [r, g, b].map(x => x.toString(16).padStart(2, '0')).join('');
  
    const [r1, g1, b1] = hexToRgb(color1);
    const [r2, g2, b2] = hexToRgb(color2);
  
    const r = Math.round(r1 + (r2 - r1) * t);
    const g = Math.round(g1 + (g2 - g1) * t);
    const b = Math.round(b1 + (b2 - b1) * t);
  
    return rgbToHex(r, g, b);
  }
  


}
