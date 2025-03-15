import { Injectable } from '@angular/core';
import { AbstractDataService } from '../abstract-data.service';
import { Observable, of } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { LoggerService } from '../logger.service';
import { User } from '../../models/models';

@Injectable({
  providedIn: 'root'
})
export class UserService extends AbstractDataService<User> {

  constructor(private logger: LoggerService, client: HttpClient) {
    super('users', client);
  }

  lockUser(user: User): Observable<User> {
    return this.client.get(this.baseUrl + '/' + this.root_api + '/' + user.id + '/lock', { withCredentials: true });
  }

  unlockUser(user: User): Observable<User> {
    return this.client.get(this.baseUrl + '/' + this.root_api + '/' + user.id + '/unlock', { withCredentials: true });
  }
}
