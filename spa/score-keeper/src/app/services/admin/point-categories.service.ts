import { Injectable } from '@angular/core';
import { LoggerService } from '../logger.service';
import { HttpClient } from '@angular/common/http';
import { Grade, PointCategory } from '../../models/models';
import { AbstractDataService } from '../abstract-data.service';

@Injectable({
  providedIn: 'root'
})
export class PointCategoriesService extends AbstractDataService<PointCategory>{

  constructor(private logger: LoggerService, client: HttpClient) {
      super('point_categories', client);
    }
}
