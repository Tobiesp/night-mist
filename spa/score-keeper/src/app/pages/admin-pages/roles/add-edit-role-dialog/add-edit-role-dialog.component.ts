import { Component, inject, Inject, signal } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { AdminService } from '../../../../services/admin.service';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { map, Observable, startWith } from 'rxjs';
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { MatChipInputEvent } from '@angular/material/chips';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { Role } from '../../../../services/admin/role.service';

export interface dialogData {
  type: 'add' | 'edit';
  role: Role;
}

@Component({
  selector: 'app-add-edit-role-dialog',
  templateUrl: './add-edit-role-dialog.component.html',
  styleUrl: './add-edit-role-dialog.component.css',
  standalone: false
})
export class AddEditRoleDialogComponent {
  readonly separatorKeysCodes: number[] = [ENTER, COMMA];
  readonly privileges = signal<string[]>([]);
  readonly announcer = inject(LiveAnnouncer);
  roleForm!: FormGroup;
  role: Role;
  privAutoCtrl = new FormControl('');
  privilegesOptions: string[] = [];
  filteredOptions!: Observable<string[]>;
  invalidPrivileges = false;

constructor(
    public dialogRef: MatDialogRef<AddEditRoleDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: dialogData,
    private fb: FormBuilder,
    private adminService: AdminService
  ) {
    this.role = data?.role;
    this.adminService.getAllPrivileges().subscribe({
      next: (privileges: string[]) => {
        this.privilegesOptions = privileges;
      },
      error: (error: any) => {
        console.error(error);
      }
    });
  }
  
  ngOnInit(): void {
    this.roleForm = this.fb.group({
      rolename: [this.role.role, Validators.required]
    });
    this.filteredOptions = this.privAutoCtrl.valueChanges.pipe(
      startWith(''),
      map(value => this._filter(value || '')),
    );
    this.privileges.update(privileges => this.role?.privileges || []);
  }

  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.privilegesOptions
          .filter(option => option.toLowerCase().includes(filterValue))
          .filter(option => !this.privileges().includes(option));
  }
  
  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();

    // Add our privilege
    if (value) {
      this.privileges.update(privileges => [...privileges, value]);
    }

    // Clear the input value
    this.privAutoCtrl.setValue('');
  }

  remove(item: string): void {
    this.privileges.update(privileges => {
      const index = privileges.indexOf(item);
      if (index < 0) {
        return privileges;
      }

      privileges.splice(index, 1);
      this.announcer.announce(`Removed ${item}`);
      return [...privileges];
    });
  }

  selected(event: MatAutocompleteSelectedEvent): void {
    this.privileges.update(privileges => [...privileges, event.option.viewValue]);
    this.privAutoCtrl.setValue('');
    event.option.deselect();
  }


  onCancel(): void {
    this.dialogRef.close(null);
  }

  onConfirm(): void {
    if (this.roleForm.invalid) {
      return;
    }
    if (this.privileges().length === 0) {
      this.invalidPrivileges = true;
      return;
    }
    this.role.role = this.roleForm.value.rolename;
    this.role.privileges = this.privileges();
    console.log(JSON.stringify(this.role));
    this.dialogRef.close(this.role);
  }
}
