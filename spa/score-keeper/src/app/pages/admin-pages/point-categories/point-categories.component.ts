import { Component } from '@angular/core';
import { PointCategory } from '../../../models/models';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { PointCategoriesService } from '../../../services/admin/point-categories.service';
import { MatDialog } from '@angular/material/dialog';
import { ErrorDialogService } from '../../../services/error-dialog.service';
import { PointCategoriesEditDialogComponent } from './point-categories-edit-dialog/point-categories-edit-dialog.component';

@Component({
  selector: 'app-point-categories',
  templateUrl: './point-categories.component.html',
  styleUrl: './point-categories.component.css',
  standalone: false
})
export class PointCategoriesComponent {

  categories: PointCategory[] = [];
  categoryForm!: FormGroup;

  constructor(
      private categoriesService: PointCategoriesService,
      private errorService: ErrorDialogService,
      public dialog: MatDialog,) {
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
    this.categoryForm = new FormGroup({
      category_name: new FormControl('', [Validators.required]),
      category_description: new FormControl('', [Validators.required])
    });
  }

  addCategory() {
    if (this.categoryForm.valid) {
      const  tmp = {
        category_name: this.categoryForm.get('category_name')?.value,
        description: this.categoryForm.get('category_description')?.value,
        deleted: false
      }
      this.categoriesService.create(tmp).subscribe({
        next: (category: PointCategory) => {
          this.categories.push(category);
          this.categoryForm.reset();
        },
        error: (error: any) => {
          this.errorService.showErrorDialog(`Error creating category: ${JSON.stringify(error.error)}`, error.status);
        }
      });
    }
  }

  editCategory(category: PointCategory) {
    this.dialog.open(PointCategoriesEditDialogComponent, {
      data: category,
      width: '500px'
    }).afterClosed().subscribe((result) => {
      if (result) {
        this.categoriesService.update(result).subscribe({
          next: (category: PointCategory) => {
            const index = this.categories.findIndex((c) => c.id === category.id);
            this.categories[index] = category;
          }, 
          error: (error: any) => {
            this.errorService.showErrorDialog(`Error updating category: ${JSON.stringify(error.error)}`, error.status);
          }
        });
      }
    });
  }

  removeCategory(category: PointCategory) {
    const id = category.id;
    if (id) {
      this.categoriesService.delete(id).subscribe({
        next: () => {
          this.categories = this.categories.filter(c => c.id !== id);
        },
        error: (error: any) => {
          this.errorService.showErrorDialog(`Error deleting category: ${JSON.stringify(error.error)}`, error.status);
        }
      });
    }
  }

}
