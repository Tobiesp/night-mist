import { Component, EventEmitter, Input, Output } from '@angular/core';
import { LoggerService } from '../../services/logger.service';
import { AuthService } from '../../services/auth/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-menu-header',
  templateUrl: './menu-header.component.html',
  styleUrl: './menu-header.component.css',
  standalone: false,
})
export class MenuHeaderComponent {
  authservice: AuthService;
  logger: LoggerService;
  router: Router;
  @Input() title: string = '';
  @Output() toggleMenu = new EventEmitter<boolean>()
  hideMenu: boolean = false;
  
  constructor(
    authService: AuthService,
    logger: LoggerService,
    router: Router
  ) { 
    this.authservice = authService;
    this.logger = logger;
    this.router = router;
    logger.debug('MenuHeaderComponent created');
  }

  logout(): void {
    this.authservice.logout();
    this.router.navigate(['/login']);
  }

  toggleMenuAction(): void {
    this.hideMenu = !this.hideMenu;
    this.toggleMenu.emit(this.hideMenu);
  }
}
