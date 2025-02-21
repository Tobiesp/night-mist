import { Component, EventEmitter, Input, OnInit, Output, ViewChild } from '@angular/core';
import { LoggerService } from '../../services/logger.service';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { MatIcon } from '@angular/material/icon';

@Component({
  selector: 'app-menu-header',
  templateUrl: './menu-header.component.html',
  styleUrl: './menu-header.component.css',
  standalone: false,
})
export class MenuHeaderComponent implements OnInit {

  hideMenu: boolean = false;
  authservice: AuthService;
  logger: LoggerService;
  router: Router;
  @Input() title: string = '';
  @Output() toggleMenu = new EventEmitter<boolean>()
  
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

  ngOnInit(): void {
    this.hideMenu = !this.authservice.isLoggedIn();
    this.logger.debug(`User logged in: ${this.authservice.isLoggedIn()}; hide menu: ${this.hideMenu}`);
  }

  logout(): void {
    this.authservice.logout();
    this.hideMenu = true;
    this.router.navigate(['/login']);
  }

  toggleMenuAction(): void {
    this.hideMenu = !this.hideMenu;
    this.toggleMenu.emit(this.hideMenu);
  }

}
