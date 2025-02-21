import { Component, ViewChild } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { LoggerService } from '../../services/logger.service';
import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';
import { SnackbarComponent } from '../../components/snackbar/snackbar.component';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
  standalone: false
})
export class LoginComponent {
  loginForm!: FormGroup;

  @ViewChild('LoginSnackbarComponent') snackbar!: SnackbarComponent;

  constructor(
    private authService: AuthService,
    private router: Router,
    private logger: LoggerService,
    private fb: FormBuilder
  ) { }

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      this.authService.login(this.loginForm.value.username, this.loginForm.value.password).subscribe({
        next: () => {
          console.log(this.loginForm.value);
          this.router.navigate(['/home']);
        },
        error: (err) => {
          this.logger.error(err);
          this.snackbar!.message = 'Invalid username or password';
          this.snackbar!.level = 'error';
          this.snackbar!.openSnackBar();
        }
      });
    } else {
      this.snackbar!.message = 'Invalid username or password';
      this.snackbar!.level = 'error';
      this.snackbar!.openSnackBar();
      this.logger.error('Form is invalid');
      this.logger.error(JSON.stringify(this.loginForm.errors));
    } 
  }

}
