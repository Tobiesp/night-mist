import { Component, Inject } from '@angular/core';
import { Grade, StudentGroup } from '../../../../models/models';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { GradeService } from '../../../../services/admin/grade.service';
import { ErrorDialogService } from '../../../../services/error-dialog.service';

export interface userDialogData {
  group: StudentGroup;
}

@Component({
  selector: 'app-edit-student-group-dialog',
  templateUrl: './edit-student-group-dialog.component.html',
  styleUrl: './edit-student-group-dialog.component.css',
  standalone: false
})
export class EditStudentGroupDialogComponent {

  group: StudentGroup;
  groupsForm!: FormGroup;
  grades: Grade[] = [];

constructor(
    public dialogRef: MatDialogRef<EditStudentGroupDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: userDialogData,
    private fb: FormBuilder,
    private gradeService: GradeService,
    private errorService: ErrorDialogService,
  ) {
    this.group = data?.group;
    this.gradeService.getAll().subscribe({
      next: (data) => {
        this.grades = data;
      },
      error: (error) => {
        this.errorService.showErrorDialog(`Error loading grades: ${error.error.error}`, error.status);
      }
    });
  }

  ngOnInit(): void {
    this.groupsForm = this.fb.group({
      group_name: [this.group.group_name, Validators.required],
      grades: [this.group.grades, Validators.required]
    });

    // select all grades in the dropdown list which are present in the group.grades object
    this.groupsForm.get('grades')?.setValue(this.group.grades);
  }

  onSave() {
    if (this.groupsForm.valid) {
      this.group.group_name = this.groupsForm.get('group_name')?.value;
      this.group.grades = this.groupsForm.get('grades')?.value;
    }
    this.dialogRef.close(this.group);
  }

  onCancel(): void {
    this.dialogRef.close(null);
  }

}
