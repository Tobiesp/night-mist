import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { PointCategory } from '../../../../models/models';
import { PointCategoriesService } from '../../../../services/admin/point-categories.service';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ErrorDialogService } from '../../../../services/error-dialog.service';

@Component({
  selector: 'app-point-categories-edit-dialog',
  templateUrl: './point-categories-edit-dialog.component.html',
  styleUrl: './point-categories-edit-dialog.component.css',
  standalone: false
})
export class PointCategoriesEditDialogComponent {

  category: PointCategory;
  categoryForm!: FormGroup;
  
  constructor(
      public dialogRef: MatDialogRef<PointCategoriesEditDialogComponent>,
      @Inject(MAT_DIALOG_DATA) public data: PointCategory,
      private fb: FormBuilder,
      private categoriesService: PointCategoriesService,
      private errorService: ErrorDialogService,
    ) {
      this.category = data;
    }

    ngOnInit(): void {
      this.categoryForm = this.fb.group({
        category_name: [this.category.category_name, [Validators.required]],
        category_description: [this.category.description, [Validators.required]]
      });
    }

    onSave() {
      if (this.categoryForm.valid) {
        this.category.category_name = this.categoryForm.get('category_name')?.value;
        this.category.description = this.categoryForm.get('category_description')?.value;
        this.dialogRef.close(this.category);
      }
    }

    onCancel(): void {
      this.dialogRef.close(null);
    }

}
