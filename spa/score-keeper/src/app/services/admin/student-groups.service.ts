import { Injectable } from '@angular/core';
import { StudentGroup } from '../../models/models';
import { HttpClient } from '@angular/common/http';
import { AbstractDataService } from '../abstract-data.service';
import { LoggerService } from '../logger.service';

@Injectable({
  providedIn: 'root'
})
export class StudentGroupsService extends AbstractDataService<StudentGroup>{

  constructor(private logger: LoggerService, client: HttpClient) {
      super('student_groups', client);
    }
}
