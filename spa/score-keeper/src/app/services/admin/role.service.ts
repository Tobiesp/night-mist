import { Injectable } from '@angular/core';
import { AbstractDataService } from '../abstract-data.service';
import { Role } from '../../models/models';
import { HttpClient } from '@angular/common/http';
import { LoggerService } from '../logger.service';

@Injectable({
  providedIn: 'root'
})
export class RoleService extends AbstractDataService<Role> {
  constructor(private logger: LoggerService, client: HttpClient) {
    super('roles', client);
  }
}
