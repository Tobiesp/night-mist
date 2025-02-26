import { Component, ViewChild } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';
import { Router } from '@angular/router';
import { LoggerService } from '../../services/logger.service';
import { FormGroup, Validators, FormBuilder } from '@angular/forms';
import { SnackbarComponent } from '../../components/snackbar/snackbar.component';
import { MatDialog } from '@angular/material/dialog';
import { ForgotPasswordDialogComponent } from './forgot-password-dialog/forgot-password-dialog.component';
import { SignupDialogComponent } from './signup-dialog/signup-dialog.component';

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
    private fb: FormBuilder,
    public dialog: MatDialog,
  ) { }

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]]
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

  openSignupDialog(): void {
    const dialogRef = this.dialog.open(SignupDialogComponent, {
      width: '500px',
      height: '530px',
      data: { }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result !== null) {
        const data = result;
        if (data) {
          this.authService.signup(data['username'], data['email'], data['password']).subscribe({
            next: () => {
              this.snackbar!.message = 'User created';
              this.snackbar!.level = 'info';
              this.snackbar!.openSnackBar();
            },
            error: (err) => {
              this.logger.error(err);
              this.snackbar!.message = 'Error creating user';
              this.snackbar!.level = 'error';
              this.snackbar!.openSnackBar();
            }
          });
        }
      }
    });
  }

  openForgotPasswordDialog(): void {
    const dialogRef = this.dialog.open(ForgotPasswordDialogComponent, {
      width: '500px',
      height: '400px',
      data: { }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result !== null) {
        const data = result;
        if (data) {
          this.authService.forgotPassword(data['username'], data['email']).subscribe({
            next: () => {
              this.snackbar!.message = 'Password reset email sent';
              this.snackbar!.level = 'info';
              this.snackbar!.openSnackBar();
            },
            error: (err) => {
              this.logger.error(err);
              this.snackbar!.message = 'Error sending password reset email';
              this.snackbar!.level = 'error';
              this.snackbar!.openSnackBar();
          }
        });
        }
      }
    });
  }

}
