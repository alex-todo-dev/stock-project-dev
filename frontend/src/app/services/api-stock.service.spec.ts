import { TestBed } from '@angular/core/testing';

import { ApiStockService } from './api-stock.service';

describe('ApiStockService', () => {
  let service: ApiStockService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ApiStockService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
