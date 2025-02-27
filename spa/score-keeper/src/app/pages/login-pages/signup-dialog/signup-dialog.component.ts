import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-signup-dialog',
  templateUrl: './signup-dialog.component.html',
  styleUrls: ['./signup-dialog.component.css'],
  standalone: false
})
export class SignupDialogComponent {
  signupForm!: FormGroup;
  confirmPasswordValid = true;

  constructor(
      public dialogRef: MatDialogRef<SignupDialogComponent>,
      private fb: FormBuilder) {}

  ngOnInit(): void {
    this.signupForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [
      Validators.required,
      Validators.minLength(8),
      Validators.maxLength(30),
      Validators.pattern('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*]).*$')
      ]],
      confirmPassword: ['', Validators.required]
    });
  }

  onCancel(): void {
    this.dialogRef.close(null);
  }

  onConfirm(): void {
    if (this.signupForm.invalid) {
      return;
    }
    if (this.signupForm.value.password !== this.signupForm.value.confirmPassword) {
      this.confirmPasswordValid = false;
      this.signupForm.controls['confirmPassword'].setErrors({ 'incorrect': true });
      return;
    }
    const signupData = {
      username: this.signupForm.value.username,
      email: this.signupForm.value.email,
      password: this.signupForm.value.password,
      confirmPassword: this.signupForm.value.confirmPassword
    };
    this.dialogRef.close(signupData);
  }
}
