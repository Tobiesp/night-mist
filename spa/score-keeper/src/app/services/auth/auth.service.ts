import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { LoggerService } from '../logger.service';
import { Router } from '@angular/router';
import { BaseService } from '../base.service';
import { HttpClient } from '@angular/common/http';
import { User } from '../../models/models';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface SignupRequest {
  first_name: string;
  last_name: string;
  username: string;
  email: string;
  password: string;
  repeat_password: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService extends BaseService {

  constructor(private logger: LoggerService,
    private router: Router,
    private client: HttpClient
  ) {
    super();
  }

  login(username: string, password: string): Observable<boolean> {
    const req = {
      username: username,
      password: password
    }
    return new Observable<boolean>(observer => {
      const request = this.client.post<User>(this.baseUrl + '/login', req, { withCredentials: true });
      request.subscribe({
        next: (data) => {
          if (data) {
            this.setAuthState(data);
            observer.next(true);
          }
          else {
            this.removeAuthState();
            observer.next(false);
          }
          observer.complete();
        },
        error: (error) => {
          this.removeAuthState();
          observer.next(false);
          observer.complete();
        }
      });
    });
  }

  private setAuthState(user: User): void {
    localStorage.setItem('currentUser', JSON.stringify(user));
  }

  private removeAuthState(): void {
    localStorage.removeItem('currentUser');
  }

  getAuthState(): User | null {
    const user = localStorage.getItem('currentUser');
    return user ? JSON.parse(user) : null;
  }

  logout(): void {
    this.client.get(this.baseUrl + '/logout', { withCredentials: true });
    this.removeAuthState();
    document.cookie = 'session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    this.router.navigate(['/login']);
  }

  public get currentUserValue(): User | null {
    return this.getAuthState();
  }

  public isLoggedIn(): boolean {
    if (this.currentUserValue) {
      return true;
    }
    return false;
  }

  public isAuthorized(allowedPriviledges: string[]): boolean {
    const user = this.currentUserValue;
    if (!user) return false;
    if (!user.role?.priviledges) return false;
    if (user.role?.priviledges.filter(priviledge => priviledge.priviledge_name === "admin").length > 0) return true;
    return user.role?.priviledges.some(priviledge => allowedPriviledges.filter(allowed => allowed === priviledge.priviledge_name).length > 0);
  }

  public forgotPassword(username: string, email: string): Observable<Object> {
    return new Observable<Object>(observer => {
      this.client.post(this.baseUrl + '/forgot-password', { username: username, email: email }).subscribe({
        next: (data) => {
          observer.next({});
          observer.complete();
        },
        error: (error) => {
          observer.error(error);
        }
      });
    });
  }

  public signup(form: SignupRequest): Observable<Object> {
    return new Observable<Object>(observer => {
      this.client.post(this.baseUrl + '/signup', form).subscribe({
        next: (data) => {
          observer.next({});
          observer.complete();
        },
        error: (error) => {
          observer.error(error);
        }
      });
    });
  }
}
