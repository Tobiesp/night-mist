import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { LoggerService } from '../logger.service';
import { BaseService } from '../base.service';
import { Priviledge } from '../../models/models';
import { HttpClient } from '@angular/common/http';

export interface RolesResponse {
  roles: string[];
}

@Injectable({
  providedIn: 'root'
})
export class AdminService extends BaseService {

  constructor(private logger: LoggerService, private client: HttpClient) {
    super();
  }

  getAllPrivileges(): Observable<Priviledge[]> {
    return this.client.get<Priviledge[]>(this.baseUrl + '/priviledges', { withCredentials: true });
  }
}

