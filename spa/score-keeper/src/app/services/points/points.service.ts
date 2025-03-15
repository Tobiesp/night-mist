import { Injectable } from '@angular/core';
import { Point } from '../../models/models';
import { HttpClient } from '@angular/common/http';
import { AbstractDataService } from '../abstract-data.service';
import { LoggerService } from '../logger.service';

@Injectable({
  providedIn: 'root'
})
export class PointsService extends AbstractDataService<Point>{

  constructor(private logger: LoggerService, client: HttpClient) {
      super('points', client);
    }
}
