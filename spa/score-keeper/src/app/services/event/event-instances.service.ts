import { Injectable } from '@angular/core';
import { EventInstance } from '../../models/models';
import { HttpClient } from '@angular/common/http';
import { AbstractDataService } from '../abstract-data.service';
import { LoggerService } from '../logger.service';

@Injectable({
  providedIn: 'root'
})
export class EventInstancesService extends AbstractDataService<EventInstance>{

  constructor(private logger: LoggerService, client: HttpClient) {
      super('events/instances', client);
    }
}
