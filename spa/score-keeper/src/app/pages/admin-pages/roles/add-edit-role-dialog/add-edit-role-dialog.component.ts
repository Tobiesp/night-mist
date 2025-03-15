import { Component, inject, Inject, signal } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { AdminService } from '../../../../services/admin/admin.service';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { map, Observable, startWith } from 'rxjs';
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { MatChipInputEvent } from '@angular/material/chips';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { Priviledge, Role } from '../../../../models/models';

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
  readonly priviledges = signal<Priviledge[]>([]);
  readonly announcer = inject(LiveAnnouncer);
  roleForm!: FormGroup;
  role: Role;
  privAutoCtrl = new FormControl('');
  privilegdesOptions: Priviledge[] = [];
  filteredOptions!: Observable<Priviledge[]>;
  invalidPrivileges = false;

constructor(
    public dialogRef: MatDialogRef<AddEditRoleDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: dialogData,
    private fb: FormBuilder,
    private adminService: AdminService
  ) {
    this.role = data?.role;
    this.adminService.getAllPrivileges().subscribe({
      next: (privileges: Priviledge[]) => {
        this.privilegdesOptions = privileges;
      },
      error: (error: any) => {
        console.error(error);
      }
    });
  }
  
  ngOnInit(): void {
    this.roleForm = this.fb.group({
      rolename: [this.role.role_name, Validators.required]
    });
    this.filteredOptions = this.privAutoCtrl.valueChanges.pipe(
      startWith(''),
      map(value => this._filter(value || '')),
    );
    this.priviledges.update(privileges => this.role?.priviledges || []);
  }

  private _filter(value: string): Priviledge[] {
    const filterValue = value.toLowerCase();

    return this.privilegdesOptions
          .filter(option => option.priviledge_name.toLowerCase().includes(filterValue))
          .filter(option => !this.priviledges().includes(option));
  }
  
  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();
    const p = this.privilegdesOptions.find(p => p.priviledge_name === value);

    // Add our privilege
    if (p) {
      this.priviledges.update(privilegdes => [...privilegdes, p]);
    }

    // Clear the input value
    this.privAutoCtrl.setValue('');
  }

  remove(item: string): void {
    const p = this.privilegdesOptions.find(p => p.priviledge_name === item);
    if (!p) {
      return;
    }
    this.priviledges.update(priviledges => {
      const index = priviledges.indexOf(p);
      if (index < 0) {
        return priviledges;
      }

      priviledges.splice(index, 1);
      this.announcer.announce(`Removed ${item}`);
      return [...priviledges];
    });
  }

  selected(event: MatAutocompleteSelectedEvent): void {
    const p = this.privilegdesOptions.find(p => p.priviledge_name === event.option.viewValue);
    if (!p) {
      return;
    }
    this.priviledges.update(privileges => [...privileges, p]);
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
    if (this.priviledges().length === 0) {
      this.invalidPrivileges = true;
      return;
    }
    this.role.role_name = this.roleForm.value.rolename;
    this.role.priviledges = this.priviledges();
    console.log(JSON.stringify(this.role));
    this.dialogRef.close(this.role);
  }
}
