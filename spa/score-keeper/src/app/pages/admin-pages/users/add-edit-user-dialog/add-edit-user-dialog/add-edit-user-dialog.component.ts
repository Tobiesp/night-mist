import { Component, inject, Inject, signal } from '@angular/core';
import { Priviledge, Role, User } from '../../../../../services/auth/auth.service';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { ENTER, COMMA } from '@angular/cdk/keycodes';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { RoleService } from '../../../../../services/admin/role.service';
import { LoggerService } from '../../../../../services/logger.service';

export interface userDialogData {
  type: 'add' | 'edit';
  user: User;
}

@Component({
  selector: 'app-add-edit-user-dialog',
  templateUrl: './add-edit-user-dialog.component.html',
  styleUrl: './add-edit-user-dialog.component.css',
  standalone: false
})
export class AddEditUserDialogComponent {
readonly separatorKeysCodes: number[] = [ENTER, COMMA];
  readonly privileges = signal<Priviledge[]>([]);
  userForm!: FormGroup;
  user: User;
  type = '';
  roles: Role[] = [];
  confirmPasswordInvalid = false;

constructor(
    public dialogRef: MatDialogRef<AddEditUserDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: userDialogData,
    private fb: FormBuilder,
    public roleService: RoleService,
    public logger: LoggerService
  ) {
    this.user = data?.user;
    this.type = data?.type;
  }
  
  ngOnInit(): void {
    this.roleService.getAll().subscribe({
      next: (data) => {
        this.roles = data;
      },
      error: (error) => {
        this.logger.error(`Error loading roles: ${error}`);
      }
    });
    if (this.type === 'add') {
      this.userForm = this.fb.group({
        username: [this.user.username, Validators.required],
        firstname: [this.user.firstname, Validators.required],
        lastname: [this.user.lastname, Validators.required],
        email: [this.user.email, [Validators.required, Validators.email]],password: ['', [
          Validators.required,
          Validators.minLength(8),
          Validators.maxLength(30),
          Validators.pattern('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*]).*$')
          ]],
          confirmPassword: ['', Validators.required],
        role: [this.user.role?.role, Validators.required],
      });
    } else {
      this.userForm = this.fb.group({
        username: [this.user.username, Validators.required],
        firstname: [this.user.firstname, Validators.required],
        lastname: [this.user.lastname, Validators.required],
        email: [this.user.email, [Validators.required, Validators.email]],
        role: [this.user.role?.role, Validators.required],
      });
    }
  }


  onCancel(): void {
    this.dialogRef.close(null);
  }

  onConfirm(): void {
    if (this.userForm.invalid) {
      return;
    }
    const temp_user: User = {
      username: this.userForm.value.username,
      firstname: this.userForm.value.firstname,
      lastname: this.userForm.value.lastname,
      email: this.userForm.value.email,
      role: this.roles.find(role => role.role === this.userForm.value.role),
    };
    if (this.type === 'edit') {
      temp_user.id = this.user.id;
    }
    if (this.userForm.value.password !== this.userForm.value.confirmPassword) {
      this.confirmPasswordInvalid = false;
      this.userForm.controls['confirmPassword'].setErrors({ 'incorrect': true });
      return;
    }
    // TODO: Check if the user values are unqiue for a new user
    this.dialogRef.close(temp_user);
  }
}
