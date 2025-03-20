import { Injectable } from '@angular/core';
import { AbstractDataService } from '../abstract-data.service';
import { Observable, of } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { User } from '../../models/models';
import { ErrorDialogService } from '../error-dialog.service';

@Injectable({
  providedIn: 'root'
})
export class UserService extends AbstractDataService<User> {

  constructor(public logger: ErrorDialogService, client: HttpClient) {
    super('users', client);
  }

  lockUser(user: User): Observable<User> {
    return this.client.post(this.baseUrl + '/' + this.root_api + '/' + user.id + '/lock', {}, { withCredentials: true });
  }

  unlockUser(user: User): Observable<User> {
    return this.client.post(this.baseUrl + '/' + this.root_api + '/' + user.id + '/unlock', {}, { withCredentials: true });
  }
}
