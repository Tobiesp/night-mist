import { Injectable } from '@angular/core';
import { Grade } from '../../models/models';
import { AbstractDataService } from '../abstract-data.service';
import { LoggerService } from '../logger.service';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class GradeService extends AbstractDataService<Grade>{

  constructor(private logger: LoggerService, client: HttpClient) {
      super('grades', client);
    }
}
