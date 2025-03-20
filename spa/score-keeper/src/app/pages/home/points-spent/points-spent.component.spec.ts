import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PointsSpentComponent } from './points-spent.component';

describe('PointsSpentComponent', () => {
  let component: PointsSpentComponent;
  let fixture: ComponentFixture<PointsSpentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PointsSpentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PointsSpentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
