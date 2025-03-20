import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PointsEarnedComponent } from './points-earned.component';

describe('PointsEarnedComponent', () => {
  let component: PointsEarnedComponent;
  let fixture: ComponentFixture<PointsEarnedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PointsEarnedComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PointsEarnedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
