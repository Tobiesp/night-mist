import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { LoggerService } from './logger.service';
import { Router } from '@angular/router';
import { BaseServiceService } from './base-service.service';

export interface Priviledge {
  id: string;
  name: string;
}

export interface Role {
  id: string;
  role: string;
  priviledges: Priviledge[];
}

export interface User {
  id?: string;
  username?: string;
  firstname?: string;
  lastname?: string;
  email?: string;
  role?: Role;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService extends BaseServiceService {

  constructor(private logger: LoggerService,
    private router: Router
  ) {
    super();
  }

  login(username: string, password: string): Observable<boolean> {
    const priviledge = {name: username === 'admin' ? 'admin' : 'student_read', id: '1'};
    const role: Role = {
      id: '1',
      role: username === 'admin' ? 'admin' : 'student',
      priviledges: [priviledge],
    };
    const user: User = {
      username: username,
      role: role,
    };
    return new Observable<boolean>(observer => {
      if (user) {
        this.logger.info(`User ${user.username} logged in with role: ${user.role}`);
        this.setAuthState(user);
        observer.next(true);
      }
      else {
        this.logger.error(`User ${username} not found`);
        this.removeAuthState();
        observer.next(false);
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
      return true;
    }
    return false;
  }

  public isAuthorized(allowedPriviledges: string[]): boolean {
    const user = this.currentUserValue;
    if (!user) return false;
    if (!user.role?.priviledges) return false;
    if (user.role?.priviledges.filter(priviledge => priviledge.name === "admin").length > 0) return true;
    return user.role?.priviledges.some(priviledge => allowedPriviledges.filter(allowed => allowed === priviledge.name).length > 0);
  }

  public forgotPassword(username: string, email: string): Observable<Object> {
    return new Observable<Object>(observer => {
      this.logger.info(`User ${username} requested password reset. Sending email to ${username} with reset instructions`);
      observer.next({});
      observer.complete();
    });
  }

  public signup(username: string, email: string, password: string): Observable<Object> {
    return new Observable<Object>(observer => {
      this.logger.info(`User ${username} signed up with email ${email} and password ${password}`);
      observer.next({});
      observer.complete();
    });
  }
}
