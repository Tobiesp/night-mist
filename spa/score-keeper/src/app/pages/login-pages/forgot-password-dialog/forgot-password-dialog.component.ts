import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { dialogData } from '../../admin-pages/roles/add-edit-role-dialog/add-edit-role-dialog.component';

@Component({
  selector: 'app-forgot-password-dialog',
  templateUrl: './forgot-password-dialog.component.html',
  styleUrl: './forgot-password-dialog.component.css',
  standalone: false
})
export class ForgotPasswordDialogComponent {
  passwordForm!: FormGroup;

constructor(
    public dialogRef: MatDialogRef<ForgotPasswordDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: dialogData,
    private fb: FormBuilder,
  ) {
  }
  
  ngOnInit(): void {
    this.passwordForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
    });
  }


  onCancel(): void {
    this.dialogRef.close(null);
  }

  onConfirm(): void {
    if (this.passwordForm.invalid) {
      return;
    }
    const dialog_data = {
      username: this.passwordForm.value.username,
      email: this.passwordForm.value.email,
    };
    this.dialogRef.close(dialog_data);
  }
}
