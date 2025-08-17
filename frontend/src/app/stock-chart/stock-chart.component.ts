import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgxChartsModule,Color, ScaleType } from '@swimlane/ngx-charts'; 
import { ChartDataService } from '../services/chart-data.service';
import { TrackedStock } from '../models/tracked-stocks.interface';
import { chartDataLine, chartPoint } from '../models/chart-data';
import { lstmPredictionInterface } from '../models/lstm-prediction';
import { LstmPredictionDataService } from '../services/lstm-prediction-data.service';
import { ChangeDetectorRef } from '@angular/core';
@Component({
    selector: 'app-stock-chart',
    standalone: true,
    imports: [CommonModule, NgxChartsModule],
    templateUrl: './stock-chart.component.html',
    styleUrl: './stock-chart.component.css'
})
export class StockChartComponent implements OnInit {
    charTitle = 'Line Chart';
    chartData:any[] = [];
    chartLines:any[] = [];
    private cardData: TrackedStock | null = null;
    private lstmChartData: lstmPredictionInterface | null = null;
    constructor(private chartDataService: ChartDataService, 
                private lstmDataService: LstmPredictionDataService,
                private cd: ChangeDetectorRef
    ) { }
    
    ngOnInit(): void {
      let predictedPriceLine;
      let actualPricLine;
      let predictedLstmLine; 
      this.chartDataService.chartData$.subscribe(data => {
          if (data){
            this.chartData = [];
            this.cardData! = data;
            // console.log("chart update:", this.cardData);
            // Gneretaing array from the recived data
            this.charTitle = this.cardData.stock_title;
            actualPricLine = this.cardData.days_tracking.map(
              obj => ({
                name: new Date(obj.date),
                value: obj.closing_price
              })
            );
            predictedPriceLine = this.cardData.next_day_predictions.map(
              obj => ({
                name: new Date(obj.date),
                value: obj.closing_price
              })
            );
            this.chartData.push({ name: 'Actual Price', series: actualPricLine });
            this.chartData.push({ name: 'Predicted Price', series: predictedPriceLine });
            // this.reAssign();
          }
          // console.log("chart data:", this.chartData);
        });
        //  pull lstm predictions 
      this.lstmDataService.chartData$.subscribe(data =>{
        if(data){
          this.lstmChartData = data;
          console.log("Lstm data for stoc:", this.lstmChartData.next_five_day_predictions)
          predictedLstmLine = this.lstmChartData.next_five_day_predictions.map( 
            obj => ({
              name : new Date(obj.date),
              value: obj.price  
          })
        );
          this.chartData.push({ name: 'LSTM predicted', series: predictedLstmLine });
          
          
        }
          this.reAssign();
      });
     
      
    }
    public lineChartData = [
        {
          name: 'Sales 2024',
          series: [
            { name: 'Jan', value: 5000 },
            { name: 'Feb', value: 7200 },
            { name: 'Mar', value: 6100 },
            { name: 'Apr', value: 2 }
          ]
        },
        {
          name: 'Sales 2023',
          series: [
            { name: 'Jan', value: 4800 },
            { name: 'Feb', value: 6800 },
            { name: 'Mar', value: 5900 },
            { name: 'Apr', value: 8000 }
          ]
        },
        {
          name: 'Sales 2025',
          series: [
            
            { name: 'May', value: 5900 },
            { name: 'Jun', value: 8000 }
          ]
        }
      ];
    
      // colorScheme = 'vivid'; // or 'cool', 'natural', etc.
    colorScheme: Color = {
    name: 'custom',
    selectable: true,
    group: ScaleType.Ordinal,
    domain: ['#e6194b', '#3cb44b', '#4363d8'] // red, green, blue
  };

  reAssign(){
    this.chartLines = this.chartData
  }
}
