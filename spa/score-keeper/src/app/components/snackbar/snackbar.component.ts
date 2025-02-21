import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatSnackBar, MatSnackBarHorizontalPosition, MatSnackBarVerticalPosition } from '@angular/material/snack-bar';

@Component({
  selector: 'app-snackbar',
  templateUrl: './snackbar.component.html',
  styleUrl: './snackbar.component.css',
  standalone: false
})
export class SnackbarComponent {

  constructor(private _snackBar: MatSnackBar) { }

  @Input() message: string = '';
  @Input() level: 'success' | 'info' | 'error' = 'info';
  @Input() action?: string | undefined;
  @Input() horizontalPosition: MatSnackBarHorizontalPosition = 'center';
  @Input() verticalPosition: MatSnackBarVerticalPosition = 'bottom';
  @Input() duration: number = 3000;

  @Output()
  handleAction: EventEmitter<any> = new EventEmitter<any>();

  public openSnackBar(): void {
    const hasAction = Boolean(this.action);

    const snackBarRef = this._snackBar.open(this.message, hasAction ? this.action: undefined, {
      duration: this.duration,
      horizontalPosition: this.horizontalPosition,
      verticalPosition: this.verticalPosition,
      panelClass: [`${this.level}`]
    });

    if (hasAction) {
      snackBarRef.onAction().subscribe(() => {
        this.handleAction!.emit();
      });
    }
  }

}
