import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { LoggerService } from './logger.service';
import { environment } from '../../environments/environment';
import { BaseServiceService } from './base-service.service';

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

  getAllPrivileges(): Observable<string[]> {
    return new Observable<string[]>(observer => {
      observer.next([
        'admin',
        'event_read',
        'event_write',
        'user_read',
        'user_write',
        'points_read',
        'points_write',
        'student_read',
        'student_write',
        'reporter_read',
        'reporter_write',
      ]);
      observer.complete();
    });
  }
}

