import { Component, ViewChild } from '@angular/core';
import { MatDrawer } from '@angular/material/sidenav';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from './services/auth/auth.service';
import { LoggerService } from './services/logger.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  standalone: false
})
export class AppComponent {
  title = 'score-keeper';
  @ViewChild("drawer") drawer!: MatDrawer;

  constructor(private authService: AuthService, private logger: LoggerService, private router: Router) {
  }

  showMenu(menuName: string): boolean {
    if (!this.authService.isLoggedIn()) {
      return false;
    }
    switch (menuName) {
      case 'home':
        return this.authService.isAuthorized(['student_read', 'student_write']);;
      case 'admin':
        return this.authService.isAuthorized(['admin']);
      case 'points-earn':
        return this.authService.isAuthorized(['admin', 'points']);
      case 'points-spend':
        return this.authService.isAuthorized(['admin', 'points']);
      case 'events':
        return this.authService.isAuthorized(['admin', 'events']);
      case 'reporter':
        return this.authService.isAuthorized(['admin', 'reporter']);
      default:
        return false;
    }
  }

  navigateTo(route: string): void {
    this.router.navigate([route]);
    this.drawer.toggle();
  }

  handleMenuEvent(event: any): void {
    this.drawer.toggle();
  }
}
