import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material/dialog';
import { ErrorDialogService } from '../../../services/error-dialog.service';
import { EventsService } from '../../../services/event/events.service';
import { EventInstance, PointEvent } from '../../../models/models';
import { ArrayDataSource, Row, TableOptions } from '../../../components/table/table.component';
import { ConfirmDialogComponent } from '../../../components/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-list-instances-dialog',
  templateUrl: './list-instances-dialog.component.html',
  styleUrl: './list-instances-dialog.component.css',
  standalone: false
})
export class ListInstancesDialogComponent {
  
    event: PointEvent;
    instanceList: EventInstance[] = [];
    dataSource!: ArrayDataSource<EventInstance>;

    constructor(
        public dialogRef: MatDialogRef<ListInstancesDialogComponent>,
        private dialog: MatDialog,
        @Inject(MAT_DIALOG_DATA) public data: PointEvent,
        private eventService: EventsService,
        private errorService: ErrorDialogService,
      ) {
        this.event = data;
        if (this.event?.id !== undefined) {
          this.eventService.getAllEventInstances(this.event).subscribe({
            next: (value: EventInstance[]) => {
              this.instanceList = value;
              this.dataSource = new ArrayDataSource<EventInstance>(this.instanceList);
            },
            error: (error) =>  {
              dialogRef.close({})
              this.errorService.showErrorDialog(`Error loading instances: ${error.error.error}`, error.status);
            },
          });
        }
      }

      tableOptions: TableOptions = {
          sortable: true,
          pagable: true,
          pageSize: 5,
          searchable: true,
          tableActions: {
            selectRow: false,
            rowActions: [
              { icon: 'delete', event: 'deleteEvent' }
            ],
            addRow: true,
          },
          columns: [
            { name: 'ID', field: 'id', type: 'string', width: 50, sortable: false, hidden: true },
            { name: 'Event Date', field: 'event_date', type: 'string', width: 50, sortable: true, hidden: false },
            { name: 'Completed', field: 'completed', type: 'string', width: 50, sortable: true, hidden: false },
          ]
        };

        handleTableEvent(event: any): void {
          switch (event.action) {
            case 'deleteEvent':
              this.openDeleteDialog(event.row);
              break;
            default:
              break;
          }
        }
        
        openDeleteDialog(row: Row): void {
          const dialogRef = this.dialog.open(ConfirmDialogComponent, {
            width: '250px',
            data: { message: `Are you sure you want to delete the event ${row['event_name']}?`}
          });
      
          dialogRef.afterClosed().subscribe((result: boolean) => {
            if (result === true) {
              const instance = row as EventInstance;
              if (instance) {
                try {
                  this.dataSource.deleteRow(instance);
                }
                catch (error: any) {
                  const err = error as Error;
                  this.errorService.showErrorDialog(`Error deleteing event: ${err.message}`, 400);
                }
              }
            }
          });
        }

}
