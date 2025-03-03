import { ErrorHandler, Injectable, NgZone } from '@angular/core';
import { LoggerService } from '../logger.service';
import { HttpErrorResponse } from '@angular/common/http';
import { ErrorDialogService } from './error-dialog.service';

@Injectable({
  providedIn: 'root'
})
export class GlobalErrorHandlerService implements ErrorHandler{

  constructor(
    private logger: LoggerService,
    private errorDialogService: ErrorDialogService,
    private zone: NgZone,
  ) { }

  handleError(error: any) {
    // Check if it's an error from an HTTP response
    if (!(error instanceof HttpErrorResponse)) {
      error = error.rejection; // get the error object
    }
    this.zone.run(() =>
      this.errorDialogService.openDialog(
        error?.error?.message || 'Undefined client error',
        error?.status,
      ),
    );

    this.logger.error(`Error from global error handler: ${error}`);
  }
}
