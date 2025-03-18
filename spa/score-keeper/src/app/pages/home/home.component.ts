import { Component } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
  standalone: false
})
export class HomeComponent {

  showStudents = false
  showRunningTotals = false
  showPointsEarned = false
  showPointsSpent = false

  constructor (
    private service: AuthService
  ) {
    this.showRunningTotals = service.isAuthorized(['student_read'])
    this.showStudents = service.isAuthorized(['student_read'])
    this.showPointsEarned = service.isAuthorized(['point_write'])
    this.showPointsSpent = service.isAuthorized(['point_write'])
  }

}
