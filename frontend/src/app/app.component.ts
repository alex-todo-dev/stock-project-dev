import { Component , inject, OnInit} from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatDialog, MatDialogModule} from '@angular/material/dialog';
import { DisclaimerDialogComponent } from './disclaimer-dialog/disclaimer-dialog.component';
import { CardSpinnerComponent } from './card-spinner/card-spinner.component';
import { StockChartComponent } from "./stock-chart/stock-chart.component";
import { StockDetailsMetricsComponent } from "./stock-details-metrics/stock-details-metrics.component";
import { PredictedMetricsComponent } from "./predicted-metrics/predicted-metrics.component";
@Component({
    selector: 'app-root',
    standalone: true,
    imports: [MatToolbarModule, MatButtonModule, MatIconModule, CardSpinnerComponent, StockChartComponent, StockDetailsMetricsComponent, PredictedMetricsComponent],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {

  ngOnInit(): void {
    this.openDialog();
  }
  title = 'ToDo AI';

  readonly dialog = inject(MatDialog);

  openDialog() {
    const dialogRef = this.dialog.open(DisclaimerDialogComponent);

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }


}
