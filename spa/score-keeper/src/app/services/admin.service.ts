import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { LoggerService } from './logger.service';
import { environment } from '../../environments/environment';

export interface RolesResponse {
  roles: string[];
}

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private baseUrl = environment.baseUrl;

  constructor(private logger: LoggerService) { }

  getAllPrivileges(): Observable<string[]> {
    return new Observable<string[]>(observer => {
      observer.next([
        'admin',
        'event_create',
        'event_read',
        'event_write',
        'user_create',
        'user_read',
        'user_write',
        'points_earn_read',
        'points_earn_write',
        'points_spend_read',
        'points_spend_write',
        'student_create',
        'student_read',
        'student_write',
      ]);
      observer.complete();
    });
  }
}

