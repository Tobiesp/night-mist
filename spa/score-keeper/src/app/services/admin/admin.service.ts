import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { LoggerService } from '../logger.service';
import { BaseServiceService } from '../base-service.service';
import { Priviledge } from '../auth/auth.service';

export interface RolesResponse {
  roles: string[];
}

@Injectable({
  providedIn: 'root'
})
export class AdminService extends BaseServiceService {

  constructor(private logger: LoggerService) {
    super();
  }

  getAllPrivileges(): Observable<Priviledge[]> {
    return new Observable<Priviledge[]>(observer => {
      observer.next([
        {name: 'admin', id: '1'},
        {name: 'event_read', id: '1'},
        {name: 'event_write', id: '1'},
        {name: 'point_read', id: '1'},
        {name: 'point_write', id: '1'},
        {name: 'student_read', id: '1'},
        {name: 'student_write', id: '1'},
        {name: 'reporter_read', id: '1'},
        {name: 'reporter_write', id: '1'},
      ]);
      observer.complete();
    });
  }
}

