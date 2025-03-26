import { Component, Injectable, ViewChild } from '@angular/core';
import { EventsService } from '../../services/event/events.service';
import { BaseTableDataSourceModel } from '../../models/base_table_datasource_model';
import { LoggerService } from '../../services/logger.service';
import { Event, EventInstance } from '../../models/models';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../components/confirm-dialog/confirm-dialog.component';
import { TableComponent, TableOptions, Row } from '../../components/table/table.component';
import { ErrorDialogService } from '../../services/error-dialog.service';
import { AddEditUserDialogComponent } from '../admin-pages/users/add-edit-user-dialog/add-edit-user-dialog/add-edit-user-dialog.component';

@Injectable({
  providedIn: 'root'
})
export class EventDataSource extends BaseTableDataSourceModel<Event> {
  constructor(
    private eventsService: EventsService,
    logger: LoggerService
  ) {
    super(eventsService, logger);
  }

  private displayStudentGroups(event: Event): string {
    let groups = '';
    for (const group of event.student_groups) {
      groups += group.group_name + ', ';
    }
    return groups;
  }

  private displayPointCategories(event: Event): string {
    let categories = '';
    for (const category of event.point_categories) {
      categories += category.category_name + ', ';
    }
    return categories;
  }

  private displayInterval(event: Event): string {
    const result = event.interval?.repeat;
    if (result === "none") {
      return "None";
    } else if (result === "daily") {
      return "Daily" + " - " + event.interval.hour + ":" + event.interval.minute;
    } else if (result === "weekly") {
      return "Weekly" + " - " + event.interval.week_day + " - " + event.interval.hour + ":" + event.interval.minute;
    } else if (result === "monthly") {
      return "Monthly" + " - " + event.interval.month_day + " - " + event.interval.hour + ":" + event.interval.minute;
    }

    return result || '';
  }

  private displayLastInstance(instance: EventInstance | undefined): string {
    if (!instance) {
      return 'No Instances';
    }
    let result = '';
    const date_str = instance.event_date;
    if (date_str) {
      const date = new Date(date_str);
      result = date.toLocaleString();
    }
    if (instance.completed) {
      result += ' - Completed';
    } else {
      result += ' - Not Completed';
    }
    return result;
  }

  override fieldDisplay(row: Event, field: string): string {
    switch (field) {
      case 'id':
        return row.id?.toString() || '';
      case 'event_name':
        return row.event_name || '';
      case 'interval':
        return this.displayInterval(row);
      case 'student_groups':
        return this.displayStudentGroups(row);
      case 'point_categories':
        return this.displayPointCategories(row);
      case 'completed':
        return row.completed ? 'Completed' : 'Not Completed';
      case 'latest_instance':
        return this.displayLastInstance(row.latest_instance);
      case 'event_instances_count':
        return row.event_instances_count?.toString() || '';
      default:
        return '';
    }
  }
  
}

@Component({
  selector: 'app-events',
  templateUrl: './events.component.html',
  styleUrl: './events.component.css',
  standalone: false
})
export class EventsComponent {
@ViewChild ('EventTable') table!: TableComponent<Event>;
  dataSource: EventDataSource

  constructor(
    public dialog: MatDialog,
    private errorLogger: ErrorDialogService,
    logger: LoggerService,
    service: EventsService) {
      this.dataSource = new EventDataSource(service, logger);
  }

  tableOptions: TableOptions = {
    sortable: true,
    pagable: true,
    pageSize: 5,
    searchable: true,
    tableActions: {
      selectRow: false,
      rowActions: [
        { icon: 'list', event: 'listEvent'},
        { icon: 'edit', event: 'editEvent'},
        { icon: 'delete', event: 'deleteEvent' }
      ],
      addRow: true,
    },
    columns: [
      { name: 'ID', field: 'id', type: 'string', width: 50, sortable: false, hidden: true },
      { name: 'Event Name', field: 'event_name', type: 'string', width: 50, sortable: true, hidden: false },
      { name: 'Interval', field: 'interval', type: 'string', width: 50, sortable: true, hidden: false },
      { name: 'Groups', field: 'student_groups', type: 'string', width: 50, sortable: true, hidden: false },
      { name: 'Point Categories', field: 'point_categories', type: 'string', width: 50, sortable: true, hidden: false },
      { name: 'Completed', field: 'completed', type: 'string', width: 50, sortable: true, hidden: false },
      { name: 'Last Instance', field: 'latest_instance', type: 'string', width: 50, sortable: true, hidden: false },
      { name: 'Event Count', field: 'event_instances_count', type: 'string', width: 50, sortable: true, hidden: false },
    ]
  };

  handleTableEvent(event: any): void {
    console.log(JSON.stringify(event));
    if (event.action === 'editEvent') {
      this.openEditDialog(event.row);
    } else if (event.action === 'deleteEvent') {
      this.openDeleteDialog(event.row);
    } else if (event.action === 'addRowEvent') {
      this.openAddDialog();
    } else if (event.action === 'listEvent') {
      console.log('List event:', event.row);
    } else {
      console.log('Unknown event action:', event.action);
    }
  }

  openEditDialog(row: Row): void {
    const dialogRef = this.dialog.open(AddEditUserDialogComponent, {
      width: '300px',
      height: '600px',
      data: { type: 'edit', user: row }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result !== null) {
        const event = result as Event;
        if (event) {
          try {
            this.dataSource.updateRow(event);
          }
          catch (error: any) {
            const err = error as Error;
            this.errorLogger.showErrorDialog(`Error updating event: ${err.message}`, 400);
          }
        }
      }
    });
  }

  openAddDialog(): void {
    const dialogRef = this.dialog.open(AddEditUserDialogComponent, {
      width: '300px',
      height: '675px',
      data: { type: 'add', user: {} }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result !== null) {
        const event = result as Event;
        if (event) {
          this.errorLogger.logger.debug(`Adding event:${event}`);
          try {
            this.dataSource.addRow(event);
          }
          catch (error: any) {
            const err = error as Error;
            this.errorLogger.showErrorDialog(`Error creating event: ${err.message}`, 400);
          }
        }
      }
    });
  }

  openDeleteDialog(row: Row): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '250px',
      data: { message: `Are you sure you want to delete the event ${row['event_name']}?`}
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result === true) {
        const event = row as Event;
        if (event) {
          try {
            this.dataSource.deleteRow(event);
          }
          catch (error: any) {
            const err = error as Error;
            this.errorLogger.showErrorDialog(`Error deleteing event: ${err.message}`, 400);
          }
        }
      }
    });
  }

}
