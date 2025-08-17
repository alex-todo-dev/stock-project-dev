import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StockDataCardComponent } from './stock-data-card.component';

describe('StockDataCardComponent', () => {
  let component: StockDataCardComponent;
  let fixture: ComponentFixture<StockDataCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StockDataCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StockDataCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
