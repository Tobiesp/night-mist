import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditStudentGroupDialogComponent } from './edit-student-group-dialog.component';

describe('EditStudentGroupDialogComponent', () => {
  let component: EditStudentGroupDialogComponent;
  let fixture: ComponentFixture<EditStudentGroupDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditStudentGroupDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EditStudentGroupDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
