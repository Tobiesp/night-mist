import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { PointCategory, StudentGroup, PointEvent } from '../../../models/models';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ErrorDialogService } from '../../../services/error-dialog.service';
import { StudentGroupsService } from '../../../services/admin/student-groups.service';
import { PointCategoriesService } from '../../../services/admin/point-categories.service';

@Component({
  selector: 'app-add-edit-event-dialog',
  templateUrl: './add-edit-event-dialog.component.html',
  styleUrl: './add-edit-event-dialog.component.css',
  standalone: false
})
export class AddEditEventDialogComponent {

  event: PointEvent;
  eventForm!: FormGroup;
  groups: StudentGroup[] = [];
  categories: PointCategory[] = [];

  constructor(
      public dialogRef: MatDialogRef<AddEditEventDialogComponent>,
      @Inject(MAT_DIALOG_DATA) public data: PointEvent,
      private fb: FormBuilder,
      private groupService: StudentGroupsService,
      private categoryService: PointCategoriesService,
      private errorService: ErrorDialogService,
    ) {
      this.event = data;
      this.groupService.getAll().subscribe({
        next: (value: StudentGroup[]) => {
          this.groups = value;
        },
        error: (error) =>  {
          dialogRef.close({})
          this.errorService.showErrorDialog(`Error loading groups: ${error.error.error}`, error.status);
        },
      });
      this.categoryService.getAll().subscribe({
        next: (value: PointCategory[]) => {
          this.categories = value;
        },
        error: (error) =>  {
          dialogRef.close({})
          this.errorService.showErrorDialog(`Error loading categories: ${error.error.error}`, error.status);
        },
      });
    }

    ngOnInit(): void {
      this.eventForm = this.fb.group({
        event_name: ['', Validators.required],
        event_groups: ['', Validators.required],
        event_categories: ['', Validators.required],
        event_interval_repeat: ['none', Validators.required],
        event_interval_week_day: ['Sunday', [Validators.min(0), Validators.max(6)]],
        event_interval_month_day: [1, [Validators.min(1), Validators.max(31)]],
        event_interval_hour: [0, [Validators.min(0), Validators.max(23)]],
        event_interval_minute: [0, [Validators.min(0), Validators.max(59)]],
      });

      if (this.event) {
        this.eventForm.get('event_name')?.setValue(this.event.event_name);
        this.eventForm.get('event_groups')?.setValue(this.event.student_groups);
        this.eventForm.get('event_categories')?.setValue(this.event.point_categories);

        if (this.event.interval) {
          this.eventForm.get('event_interval_repeat')?.setValue(this.event.interval.repeat);
          if (this.event.interval.repeat === 'weekly') {
            this.eventForm.get('event_interval_week_day')?.setValue(this.event.interval.week_day);
          }
          if (this.event.interval.repeat === 'monthly') {
            this.eventForm.get('event_interval_month_day')?.setValue(this.event.interval.month_day);
          }
          if (this.event.interval.repeat !== 'none') {
            this.eventForm.get('event_interval_hour')?.setValue(this.event.interval.hour);
            this.eventForm.get('event_interval_minute')?.setValue(this.event.interval.minute);
          }
        }
      }
    }

    ngAfterViewInit() {
      const repeat = this.eventForm.get('event_interval_repeat')?.value;
      if (repeat === 'none') {
      this.eventForm.get('event_interval_week_day')?.disable();
      this.eventForm.get('event_interval_month_day')?.disable();
      this.eventForm.get('event_interval_hour')?.disable();
      this.eventForm.get('event_interval_minute')?.disable();
      } else if (repeat === 'daily') {
      this.eventForm.get('event_interval_week_day')?.disable();
      this.eventForm.get('event_interval_month_day')?.disable();
      this.eventForm.get('event_interval_hour')?.enable();
      this.eventForm.get('event_interval_minute')?.enable();
      } else if (repeat === 'weekly') {
      this.eventForm.get('event_interval_week_day')?.enable();
      this.eventForm.get('event_interval_month_day')?.disable();
      this.eventForm.get('event_interval_hour')?.enable();
      this.eventForm.get('event_interval_minute')?.enable();
      } else if (repeat === 'monthly') {
      this.eventForm.get('event_interval_week_day')?.disable();
      this.eventForm.get('event_interval_month_day')?.enable();
      this.eventForm.get('event_interval_hour')?.enable();
      this.eventForm.get('event_interval_minute')?.enable();
      }
    }

    repeatChange(event: any) {
      const repeat = event.value;
      if (repeat === 'none') {
        this.eventForm.get('event_interval_week_day')?.disable();
        this.eventForm.get('event_interval_month_day')?.disable();
        this.eventForm.get('event_interval_hour')?.disable();
        this.eventForm.get('event_interval_minute')?.disable();
      } else if (repeat === 'daily') {
        this.eventForm.get('event_interval_week_day')?.disable();
        this.eventForm.get('event_interval_month_day')?.disable();
        this.eventForm.get('event_interval_hour')?.enable();
        this.eventForm.get('event_interval_minute')?.enable();
      } else if (repeat === 'weekly') {
        this.eventForm.get('event_interval_week_day')?.enable();
        this.eventForm.get('event_interval_month_day')?.disable();
        this.eventForm.get('event_interval_hour')?.enable();
        this.eventForm.get('event_interval_minute')?.enable();
      } else if (repeat === 'monthly') {
        this.eventForm.get('event_interval_week_day')?.disable();
        this.eventForm.get('event_interval_month_day')?.enable();
        this.eventForm.get('event_interval_hour')?.enable();
        this.eventForm.get('event_interval_minute')?.enable();
      }
    }

    onSave() {
      if (this.eventForm.valid) {
        this.event.event_name = this.eventForm.get('event_name')?.value;
        this.event.student_groups = this.eventForm.get('event_groups')?.value;
        this.event.point_categories = this.eventForm.get('event_categories')?.value;
        if (!this.event.interval) {
          this.event.interval = {
            repeat: this.eventForm.get('event_interval_repeat')?.value,
          }
        } else {
          this.event.interval.repeat = this.eventForm.get('event_interval_repeat')?.value;
        }
        if (this.event.interval.repeat === 'weekly') {
          this.event.interval.week_day = this.eventForm.get('event_interval_week_day')?.value;
        } else if (this.event.interval.repeat === 'monthly') {
          this.event.interval.month_day = this.eventForm.get('event_interval_month_day')?.value;
        }
        if (this.event.interval.repeat !== 'none') {
          this.event.interval.hour = this.eventForm.get('event_interval_hour')?.value;
          this.event.interval.minute = this.eventForm.get('event_interval_minute')?.value;
        }
        this.dialogRef.close(this.event);
      }
    }
  
    onCancel(): void {
      this.dialogRef.close(null);
    }

}
