import { TestBed } from '@angular/core/testing';

import { PointsEarnedService } from './points-earned.service';

describe('PointsEarnedService', () => {
  let service: PointsEarnedService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PointsEarnedService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
