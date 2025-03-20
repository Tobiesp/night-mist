import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Grade, StudentGroup } from '../../../models/models';
import { GradeService } from '../../../services/admin/grade.service';
import { StudentGroupsService } from '../../../services/admin/student-groups.service';
import { ErrorDialogService } from '../../../services/error-dialog.service';
import { EditStudentGroupDialogComponent } from './edit-student-group-dialog/edit-student-group-dialog.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-student-groups',
  templateUrl: './student-groups.component.html',
  styleUrl: './student-groups.component.css',
  standalone: false
})
export class StudentGroupsComponent {
  groups: StudentGroup[] = []
  grades: Grade[] = []
  groupsForm!: FormGroup

  constructor(
    private gradeService: GradeService,
    private groupsService: StudentGroupsService,
    private errorService: ErrorDialogService,
    public dialog: MatDialog,
  ) {
    this.groupsService.getAll().subscribe({
      next: (groups: StudentGroup[]) => {
        this.groups = groups;
      },
      error: (error: any) => {
        this.errorService.showErrorDialog('Error getting groups', error.status);
      }
    });
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
    this.groupsForm = new FormGroup({
      group_name: new FormControl('', [Validators.required]),
      grades: new FormControl([], [Validators.required])
    });
  }

  displayGrades(grades: Grade[]): string {
    if (!grades) return '';
    return grades.map(g => g.grade_name).join(', ');
  }
  
  addGroup() {
    if (this.groupsForm.valid) {
      const  tmp = {
        group_name: this.groupsForm.get('group_name')?.value,
        grades: this.groupsForm.get('grades')?.value
      }
      this.groupsService.create(tmp).subscribe({
        next: (group: StudentGroup) => {
          this.groups.push(group);
          this.groupsForm.reset();
        },
        error: (error: any) => {
          this.errorService.showErrorDialog(`Error creating student group: ${JSON.stringify(error.error.error)}`, error.status);
        }
      });
    }
  }

  removeGroup(group: StudentGroup) {
    const id = group.id;
    if (id) {
      this.groupsService.delete(id).subscribe({
        next: () => {
          this.groups = this.groups.filter(g => g.id !== id);
        },
        error: (error: any) => {
          this.errorService.showErrorDialog(`Error deleting student group: ${JSON.stringify(error.error.error)}`, error.status);
        }
      });
    }
  }

  editGroup(group: StudentGroup) {
    const dialogRef = this.dialog.open(EditStudentGroupDialogComponent, {
      width: '250px',
      height: '300px',
      data: { group: group }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result !== null && result !== undefined) {
        const updatedGroup = result as StudentGroup;
        if (updatedGroup) {
          this.groupsService.update(updatedGroup).subscribe({
            next: (group: StudentGroup) => {
              this.groups = this.groups.map(g => g.id === group.id ? group : g);
            },
            error: (error: any) => {
              this.errorService.showErrorDialog(`Error updating student group: ${JSON.stringify(error.error.error)}`, error.status);
            }
          });
        }
      }
    });
  }
}
