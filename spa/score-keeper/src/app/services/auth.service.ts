import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { LoggerService } from './logger.service';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';

export interface User {
  username: string;
  priviledges: string[];
}

export interface LoginResponse {
  token: string;
  error_code: number;
  error_message: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private baseUrl = environment.baseUrl;

  constructor(private logger: LoggerService,
    private router: Router
  ) {
  }

  login(username: string, password: string): Observable<LoginResponse> {
    const user: User = {
      username: username,
      priviledges: username === 'admin' ? ['admin', 'user'] : ['user'],
    };
    return new Observable<LoginResponse>(observer => {
      if (user) {
        this.logger.info(`User ${user.username} logged in with roles: ${user.priviledges.join(', ')}`);
        this.setAuthState(user);
        observer.next({ token: '123456', error_code: 0, error_message: '' });
      }
      else {
        this.logger.error(`User ${username} not found`);
        this.removeAuthState();
        observer.next({ token: '', error_code: 401, error_message: 'User not found' });
      }
      observer.complete();
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
    this.removeAuthState();
    this.router.navigate(['/login']);
  }

  public get currentUserValue(): User | null {
    return this.getAuthState();
  }

  public isLoggedIn(): boolean {
    if (this.currentUserValue) {
      this.logger.debug(`User ${this.currentUserValue.username} is logged in`);
      return true;
    }
    return false;
  }

  public isAuthorized(allowedPriviledges: string[]): boolean {
    const user = this.currentUserValue;
    this.logger.debug(`User state: ${JSON.stringify(user)}`);
    if (!user) return false;
    this.logger.debug(`User Admin: ${user.priviledges.includes('admin')}`);
    if (user.priviledges.includes('admin')) return true;
    return user.priviledges.some(priviledge => allowedPriviledges.includes(priviledge));
  }
}
