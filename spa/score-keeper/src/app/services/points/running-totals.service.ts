import { Injectable } from '@angular/core';
import { RunningTotal } from '../../models/models';
import { HttpClient } from '@angular/common/http';
import { AbstractDataService } from '../abstract-data.service';
import { LoggerService } from '../logger.service';

@Injectable({
  providedIn: 'root'
})
export class RunningTotalsService extends AbstractDataService<RunningTotal>{

  constructor(private logger: LoggerService, client: HttpClient) {
      super('points/running-totals', client);
    }
}
