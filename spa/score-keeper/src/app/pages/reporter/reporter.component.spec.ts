import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReporterComponent } from './reporter.component';

describe('ReporterComponent', () => {
  let component: ReporterComponent;
  let fixture: ComponentFixture<ReporterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReporterComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ReporterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
