import { TestBed } from '@angular/core/testing';

import { PointCategoriesService } from './point-categories.service';

describe('PointCategoriesService', () => {
  let service: PointCategoriesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PointCategoriesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
