import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PointCategoriesComponent } from './point-categories.component';

describe('PointCategoriesComponent', () => {
  let component: PointCategoriesComponent;
  let fixture: ComponentFixture<PointCategoriesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PointCategoriesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PointCategoriesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
