import { TestBed } from '@angular/core/testing';

import { LstmPredictionDataService } from './lstm-prediction-data.service';

describe('LstmPredictionDataService', () => {
  let service: LstmPredictionDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LstmPredictionDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
