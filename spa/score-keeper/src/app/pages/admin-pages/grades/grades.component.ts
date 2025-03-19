import { Component, inject, signal } from '@angular/core';
import { GradeService } from '../../../services/admin/grade.service';
import { Grade } from '../../../models/models';
import { MatChipGrid, MatChipInputEvent } from '@angular/material/chips';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { ErrorDialogService } from '../../../services/error-dialog.service';
import { Form, FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-grades',
  templateUrl: './grades.component.html',
  styleUrl: './grades.component.css',
  standalone: false
})
export class GradesComponent {

  grades: Grade[] = []
  gradeForm!: FormGroup

  constructor(
    private gradeService: GradeService,
    private errorService: ErrorDialogService,
  ) {
    this.gradeService.getAll().subscribe({
      next: (grades: Grade[]) => {
        this.grades = grades;
      },
      error: (error: any) => {
        this.errorService.showErrorDialog('Error getting grades', error.status);
      }
    });
  }

  ngOnInit() {
    this.gradeForm = new FormGroup({
      grade_name: new FormControl('')
    });
  }
  
  addGrade() {
    if (this.gradeForm.valid && this.gradeForm.get('grade_name')?.value !== '') {
      const  tmp = {
        grade_name: this.gradeForm.get('grade_name')?.value
      }
      this.gradeService.create(tmp).subscribe({
        next: (grade: Grade) => {
          this.grades.push(grade);
          this.gradeForm.reset();
        },
        error: (error: any) => {
          this.errorService.showErrorDialog(`Error creating grade: ${JSON.stringify(error.error.error)}`, error.status);
        }
      });
    }
  }

  removeGrade(grade: Grade) {
    const id = grade.id;
    if (id) {
      this.gradeService.delete(id).subscribe({
        next: () => {
          this.grades = this.grades.filter(g => g.id !== id);
        },
        error: (error: any) => {
          this.errorService.showErrorDialog(`Error deleting grade: ${JSON.stringify(error.error.error)}`, error.status);
        }
      });
    }
  }
}
