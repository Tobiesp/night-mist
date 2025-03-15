import { Injectable } from '@angular/core';
import { PointEarned } from '../../models/models';
import { HttpClient } from '@angular/common/http';
import { AbstractDataService } from '../abstract-data.service';
import { LoggerService } from '../logger.service';

@Injectable({
  providedIn: 'root'
})
export class PointsEarnedService extends AbstractDataService<PointEarned>{

  constructor(private logger: LoggerService, client: HttpClient) {
      super('points/earned', client);
    }
}
