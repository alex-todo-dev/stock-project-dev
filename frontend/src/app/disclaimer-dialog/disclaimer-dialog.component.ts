import { Component } from '@angular/core';
import {  MatDialogClose } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';

@Component({
    selector: 'app-disclaimer-dialog',
    standalone: true,
    imports: [MatButtonModule, MatDialogClose,],
    templateUrl: './disclaimer-dialog.component.html',
    styleUrl: './disclaimer-dialog.component.css'
})
export class DisclaimerDialogComponent {

}
