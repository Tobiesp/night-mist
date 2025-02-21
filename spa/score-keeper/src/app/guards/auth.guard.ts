import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { LoggerService } from '../services/logger.service';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router, private logger: LoggerService) {}

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    const allowedPriviledges = next.data['priviledges'] as string[];
    this.logger.debug(`Checking if user is authorized with priviledges: ${allowedPriviledges.join(', ')}`);
    this.logger.debug(`User is logged in: ${this.authService.isLoggedIn()}`);
    this.logger.debug(`User has data: ${JSON.stringify(next.data)}`);
    if (!this.authService.isLoggedIn()) {
      this.logger.debug('User is not logged in');
      this.router.navigate(['/login']);
      return false;
    }
    if (this.authService.isAuthorized(allowedPriviledges)) {
      return true;
    }

    this.logger.debug('User is not authorized');
    // Redirect to the login page or some other route
    this.router.navigate(['/login']);
    return false;
  }
}