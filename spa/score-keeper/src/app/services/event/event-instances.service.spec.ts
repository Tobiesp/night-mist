import { TestBed } from '@angular/core/testing';

import { EventInstancesService } from './event-instances.service';

describe('EventInstancesService', () => {
  let service: EventInstancesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EventInstancesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
