import { Component, Inject } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Point, PointCategory, StudentGroup } from '../../../../models/models';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { PointCategoriesService } from '../../../../services/admin/point-categories.service';
import { StudentGroupsService } from '../../../../services/admin/student-groups.service';
import { ErrorDialogService } from '../../../../services/error-dialog.service';

@Component({
  selector: 'app-points-edit-dialog',
  templateUrl: './points-edit-dialog.component.html',
  styleUrl: './points-edit-dialog.component.css',
  standalone: false
})
export class PointsEditDialogComponent {

  pointForm!: FormGroup;
  groups: StudentGroup[] = [];
  categories: PointCategory[] = [];
  point: Point;
    
    constructor(
        public dialogRef: MatDialogRef<PointsEditDialogComponent>,
        @Inject(MAT_DIALOG_DATA) public data: Point,
        private fb: FormBuilder,
        private categoriesService: PointCategoriesService,
        private grousService: StudentGroupsService,
        private errorService: ErrorDialogService,
      ) {
        this.point = data;
        this.categoriesService.getAll().subscribe({
          next: (categories: PointCategory[]) => {
            this.categories = categories;
          },
          error: (error: any) => {
            this.errorService.showErrorDialog('Error getting categories', error.status);
          }
        });
        this.grousService.getAll().subscribe({
          next: (groups: StudentGroup[]) => {
            this.groups = groups;
          },
          error: (error: any) => {
            this.errorService.showErrorDialog('Error getting groups', error.status);
          }
        });
      }

  ngOnInit(): void {
    this.pointForm = new FormGroup({
      group: new FormControl(this.data.student_group, [Validators.required]),
      category: new FormControl(this.data.point_category, [Validators.required]),
      interval: new FormControl(this.data.points_interval, [Validators.required]),
      points: new FormControl(this.data.points, [Validators.required]),
    });
    this.pointForm.get('group')?.setValue(this.data.student_group);
    this.pointForm.get('category')?.setValue(this.data.point_category);
    this.pointForm.get('interval')?.setValue(this.data.points_interval);
    this.pointForm.get('points')?.setValue(this.data.points);
  }

  onSave() {
    if (this.pointForm.valid) {
      this.point.student_group = this.pointForm.get('group')?.value;
      this.point.point_category = this.pointForm.get('category')?.value;
      this.point.points_interval = this.pointForm.get('interval')?.value;
      this.point.points = this.pointForm.get('points')?.value;
      this.dialogRef.close(this.point);
    }
  }

  onCancel(): void {
    this.dialogRef.close(null);
  }

}
