import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-heading',
  templateUrl: './heading.component.html',
  styleUrl: './heading.component.css',
  standalone: false
})
export class HeadingComponent {
  @Input() text: string = '';
  @Input() size: 'small' | 'medium' | 'large' = 'medium';

  headingStyles = {
    'font-size': this.size === 'small' ? '1.5rem' : this.size === 'medium' ? '2rem' : '3rem',
    'font-family': "'DM Sans', sans-serif",
    'font-weight': 700,
  };


}
