import { TestBed } from '@angular/core/testing';

import { PointsSpentService } from './points-spent.service';

describe('PointsSpentService', () => {
  let service: PointsSpentService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PointsSpentService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
