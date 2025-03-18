import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RunningTotalsComponent } from './running-totals.component';

describe('RunningTotalsComponent', () => {
  let component: RunningTotalsComponent;
  let fixture: ComponentFixture<RunningTotalsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RunningTotalsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RunningTotalsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
