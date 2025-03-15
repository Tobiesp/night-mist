import { Injectable } from '@angular/core';
import { PointSpent } from '../../models/models';
import { HttpClient } from '@angular/common/http';
import { AbstractDataService } from '../abstract-data.service';
import { LoggerService } from '../logger.service';

@Injectable({
  providedIn: 'root'
})
export class PointsSpentService extends AbstractDataService<PointSpent>{

  constructor(private logger: LoggerService, client: HttpClient) {
      super('points/spent', client);
    }
}
