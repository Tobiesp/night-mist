import { TestBed } from '@angular/core/testing';

import { RunningTotalsService } from './running-totals.service';

describe('RunningTotalsService', () => {
  let service: RunningTotalsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RunningTotalsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
