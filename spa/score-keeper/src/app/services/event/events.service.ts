import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AbstractDataService } from '../abstract-data.service';
import { Event } from '../../models/models';
import { LoggerService } from '../logger.service';

@Injectable({
  providedIn: 'root'
})
export class EventsService extends AbstractDataService<Event>{

  constructor(private logger: LoggerService, client: HttpClient) {
      super('events', client);
    }
}
