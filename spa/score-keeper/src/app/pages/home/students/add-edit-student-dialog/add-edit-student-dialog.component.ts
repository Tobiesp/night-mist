import { Component, Inject, OnInit } from '@angular/core';
import { Grade, Student, StudentGroup } from '../../../../models/models';
import { FormBuilder, FormGroup } from '@angular/forms';
import { StudentsService } from '../../../../services/students/students.service';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { AddEditRoleDialogComponent } from '../../../admin-pages/roles/add-edit-role-dialog/add-edit-role-dialog.component';
import { StudentGroupsService } from '../../../../services/admin/student-groups.service';
import { GradeService } from '../../../../services/admin/grade.service';

export interface dialogData {
  type: 'add' | 'edit';
  student: Student;
  }

@Component({
  selector: 'app-add-edit-student-dialog',
  templateUrl: './add-edit-student-dialog.component.html',
  styleUrl: './add-edit-student-dialog.component.css',
  standalone: false
})
export class AddEditStudentDialogComponent {

  // export interface Student extends BaseModel {
  //     id: string
  //     firstname: string;
  //     lastname: string;
  //     grade: Grade;
  //     student_group: StudentGroup;
  //     created_at: string
  //     updated_at: string
  // }

  studentForm!: FormGroup;
  dialog_type: 'edit' | 'add';
  student: Student;
  groups: StudentGroup[] = [];
  grades: Grade[] = [];

  constructor(
      public dialogRef: MatDialogRef<AddEditStudentDialogComponent>,
      @Inject(MAT_DIALOG_DATA) public data: dialogData,
      private fb: FormBuilder,
      private studentsService: StudentsService,
      private groupsService: StudentGroupsService,
      private gradesService: GradeService
    ) {
      this.student = data?.student;
      this.dialog_type = data?.type || 'add';
      this.groupsService.getAll().subscribe({
        next: (value: StudentGroup[]) => {
          this.groups = value;
        },
        error: (err) =>  {
          dialogRef.close({})
          throw new Error("Failed to fetch Student Groups.")
        },
      });
      this.gradesService.getAll().subscribe({
        next: (value: Grade[]) => {
          this.grades = value;
        },
        error: (err) =>  {
          dialogRef.close({})
          throw new Error("Failed to fetch Grades.")
        },
      });
    }


  ngOnInit(): void {
    this.studentForm = this.fb.group({
      firstname: [this.student?.firstname || ''],
      lastname: [this.student?.lastname || ''],
      grade: [this.student?.grade || ''],
      student_group: [this.student?.student_group || '']
    });
  }


  onCancel(): void {
    this.dialogRef.close(null);
  }

  onConfirm(): void {
    if (this.studentForm.invalid) {
      return;
    }
    this.student.firstname = this.studentForm.value.firstname;
    this.student.lastname = this.studentForm.value.lastname;
    this.student.grade = this.studentForm.value.grade;
    this.student.student_group = this.studentForm.value.student_group;
    this.dialogRef.close(this.student);
  }

}
