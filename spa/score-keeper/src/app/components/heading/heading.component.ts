import { Component, Input, OnInit, ViewChild } from '@angular/core';

@Component({
  selector: 'app-heading',
  templateUrl: './heading.component.html',
  styleUrl: './heading.component.css',
  standalone: false
})
export class HeadingComponent implements OnInit {
  @Input() text: string = '';
  @Input() size: 'small' | 'medium' | 'large' = 'medium';
  @ViewChild("h1") h1!: HTMLElement;

  ngOnInit(): void {
    this.h1.style.fontSize = this.size === 'small' ? '1.5rem' : this.size === 'medium' ? '2rem' : '3rem';
  }

}
