import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PointsEditDialogComponent } from './points-edit-dialog.component';

describe('PointsEditDialogComponent', () => {
  let component: PointsEditDialogComponent;
  let fixture: ComponentFixture<PointsEditDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PointsEditDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PointsEditDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
