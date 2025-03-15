import { Component, inject, signal } from '@angular/core';
import { GradeService } from '../../../services/admin/grade.service';
import { Grade } from '../../../models/models';
import { MatChipGrid, MatChipInputEvent } from '@angular/material/chips';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { LiveAnnouncer } from '@angular/cdk/a11y';

@Component({
  selector: 'app-grades',
  templateUrl: './grades.component.html',
  styleUrl: './grades.component.css',
  standalone: false
})
export class GradesComponent {

  readonly grades = signal<Grade[]>([]);
  readonly separatorKeysCodes: number[] = [ENTER, COMMA];
  readonly announcer = inject(LiveAnnouncer);

  constructor(private gradeService: GradeService) { }

  ngOnInit(): void {
    this.gradeService.getAll().subscribe({
      next: (grades: Grade[]) => {
        this.grades.update(grade_list => [...grades])
      },
      error: (error: any) => {
        throw new Error(`Error getting grades: ${error}`);
      }
    });
  }

  deleteGrade(grade: Grade): void {
    if (!grade.id) {
      throw new Error('Grade id is missing');
    }
    this.grades.update(grades => {
      const index = grades.indexOf(grade);
      if (index < 0) {
        return grades;
      }

      grades.splice(index, 1);
      this.announcer.announce(`Removed ${grade.grade_name}`);
      return [...grades];
    });
  }

  addGrade(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();
    if (value) {
      const grade: Grade = { grade_name: value };
      this.gradeService.create(grade).subscribe({
        next: (data: Grade) => {
          this.grades.update(grades => [...grades, data]);
        },
        error: (error: any) => {
          throw new Error(`Failed to add grade ${grade.grade_name}: ${error}`);
        }
      });
    }
    event.chipInput!.clear();
  }

}
