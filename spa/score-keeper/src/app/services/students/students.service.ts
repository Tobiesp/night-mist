import { Injectable } from '@angular/core';
import { Student } from '../../models/models';
import { HttpClient } from '@angular/common/http';
import { AbstractDataService } from '../abstract-data.service';
import { LoggerService } from '../logger.service';

@Injectable({
  providedIn: 'root'
})
export class StudentsService extends AbstractDataService<Student>{

  constructor(private logger: LoggerService, client: HttpClient) {
      super('students', client);
    }
}
