import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PointCategoriesEditDialogComponent } from './point-categories-edit-dialog.component';

describe('PointCategoriesEditDialogComponent', () => {
  let component: PointCategoriesEditDialogComponent;
  let fixture: ComponentFixture<PointCategoriesEditDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PointCategoriesEditDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PointCategoriesEditDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
