import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddEditStudentDialogComponent } from './add-edit-student-dialog.component';

describe('AddEditStudentDialogComponent', () => {
  let component: AddEditStudentDialogComponent;
  let fixture: ComponentFixture<AddEditStudentDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddEditStudentDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddEditStudentDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
