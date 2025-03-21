import { Component } from '@angular/core';
import { Interval, Point, PointCategory, Student, StudentGroup } from '../../../models/models';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { PointCategoriesService } from '../../../services/admin/point-categories.service';
import { StudentGroupsService } from '../../../services/admin/student-groups.service';
import { ErrorDialogService } from '../../../services/error-dialog.service';
import { PointsService } from '../../../services/points/points.service';
import { repeat } from 'rxjs';
import { PointsEditDialogComponent } from './points-edit-dialog/points-edit-dialog.component';

@Component({
  selector: 'app-points',
  templateUrl: './points.component.html',
  styleUrl: './points.component.css',
  standalone: false
})
export class PointsComponent {

  points: Point[] = [];
  pointForm!: FormGroup;
  groups: StudentGroup[] = [];
  categories: PointCategory[] = [];

  constructor(
      private pointsService: PointsService,
      private errorService: ErrorDialogService,
      private groupsService: StudentGroupsService,
      private categoriesService: PointCategoriesService,
      public dialog: MatDialog,) {
        this.pointsService.getAll().subscribe({
          next: (points: Point[]) => {
            this.points = points;
          },
          error: (error: any) => {
            this.errorService.showErrorDialog('Error getting points', error.status);
          }
        });
        this.groupsService.getAll().subscribe({
          next: (groups: StudentGroup[]) => {
            this.groups = groups;
          },
          error: (error: any) => {
            this.errorService.showErrorDialog('Error getting groups', error.status);
          }
        });
        this.categoriesService.getAll().subscribe({
          next: (categories: PointCategory[]) => {
            this.categories = categories;
          },
          error: (error: any) => {
            this.errorService.showErrorDialog('Error getting categories', error.status);
          }
        });
      }

  ngOnInit() {
    this.pointForm = new FormGroup({
      group: new FormControl('', [Validators.required]),
      category: new FormControl('', [Validators.required]),
      points: new FormControl('', [Validators.required, Validators.min(0)]),
      interval: new FormControl('none', [Validators.required])
    });
  }

  addPoint() {
    if (this.pointForm.valid) {
      const  tmp: Point = {
        student_group: this.pointForm.get('group')?.value,
        point_category: this.pointForm.get('category')?.value,
        points_interval: this.pointForm.get('interval')?.value,
        points: this.pointForm.get('points')?.value,
        deleted: false
      }
      this.pointsService.create(tmp).subscribe({
        next: (point: Point) => {
          this.points.push(point);
          this.pointForm.reset();
        },
        error: (error: any) => {
          this.errorService.showErrorDialog(`Error creating point: ${JSON.stringify(error.error)}`, error.status);
        }
      });
    }
  }

  removePoint(point: Point) {
    const id = point.id;
    if (id) {
      this.pointsService.delete(id).subscribe({
        next: () => {
          this.points = this.points.filter(p => p.id !== id);
        },
        error: (error: any) => {
          this.errorService.showErrorDialog(`Error deleting point: ${JSON.stringify(error.error)}`, error.status);
        }
      });
    }
  }

  editPoint(point: Point) {
    this.dialog.open(PointsEditDialogComponent, {
      data: point,
      width: '500px'
    }).afterClosed().subscribe((result) => {
      if (result) {
        this.pointsService.update(result).subscribe({
          next: (point: Point) => {
            const index = this.points.findIndex((p) => p.id === point.id);
            this.points[index] = point;
          }, 
          error: (error: any) => {
            this.errorService.showErrorDialog(`Error updating point: ${JSON.stringify(error.error)}`, error.status);
          }
        });
      }
    });
  }

}
