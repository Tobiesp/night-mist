import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AddEditStudentDialogComponent } from '../pages/home/students/add-edit-student-dialog/add-edit-student-dialog.component';
import { ErrorDialogComponent } from '../components/error-dialog/error-dialog/error-dialog.component';
import { LoggerService } from './logger.service';

@Injectable({
  providedIn: 'root'
})
export class ErrorDialogService {

  constructor(
      public dialog: MatDialog,
      public logger: LoggerService,
    ) { }

  showErrorDialog(message: string, status_code: number = 500, height: string = '300px') {
    const dialogRef = this.dialog.open(ErrorDialogComponent, {
          width: '600px',
          height: height,
          data: { message: message, status: status_code }
        });
  }
}
