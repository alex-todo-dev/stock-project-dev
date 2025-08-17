import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictedMetricsComponent } from './predicted-metrics.component';

describe('PredictedMetricsComponent', () => {
  let component: PredictedMetricsComponent;
  let fixture: ComponentFixture<PredictedMetricsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PredictedMetricsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PredictedMetricsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
