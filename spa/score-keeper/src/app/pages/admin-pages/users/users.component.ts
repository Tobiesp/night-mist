import { Component, Injectable, ViewChild } from '@angular/core';
import { Observable } from 'rxjs';
import { BaseDataSource, Row, TableComponent, TableOptions } from '../../../components/table/table.component';
import { UserService } from '../../../services/admin/user.service';
import { User } from '../../../services/auth/auth.service';
import { LoggerService } from '../../../services/logger.service';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../../components/confirm-dialog/confirm-dialog.component';
import { AddEditUserDialogComponent } from './add-edit-user-dialog/add-edit-user-dialog/add-edit-user-dialog.component';

@Injectable({
  providedIn: 'root'
})
export class UserDataSource extends BaseDataSource<User> {
  dataview: User[] = [];
  constructor(
    private roleService: UserService, 
    public logger: LoggerService
  ) {
    super();
  }

  override connect(): Observable<User[]> {
    let pageSize = 100;
    if (this.paginator) {
      pageSize = this.paginator.pageSize
    }
    this.roleService.query('', 0, pageSize, '', '').subscribe({
      next: (data) => {
        this.observable.next(data);
      },
      error: (error) => {
        this.logger.error(`Error loading user: ${error}`);
      }
    });
    return this.observable;
  }

  override disconnect(): void {
    this.observable.complete();
  }
  
  override filter(filterValue: string): void {
    const page = 0;
    let pageSize = 100;
    if (this.paginator) {
      pageSize = this.paginator.pageSize;
    }
    let sortActive = '';
    let sortDirection = '';
    if (this.sorter) {
      sortActive = this.sorter.active;
      sortDirection = this.sorter.direction;
    }
    this.roleService.query(filterValue, page, pageSize, sortActive, sortDirection).subscribe({
      next: (data) => {
        this.observable.next(data);
      },
      error: (error) => {
        this.logger.error(`Error filtering user: ${error}`);
      }
    });
  }
  
  override sortAction(sort: { active: string; direction: string; }): void {
    let page = 0;
    let pageSize = 100;
    if (this.paginator) {
      page = this.paginator.pageIndex;
      pageSize = this.paginator.pageSize;
    }
    this.logger.debug(`Sort user: ${sort.active} ${sort.direction}`);
    this.roleService.query('', page, pageSize, sort.active, sort.direction).subscribe({
      next: (data) => {
        this.observable.next(data);
      },
      error: (error) => {
        this.logger.error(`Error sort user: ${error}`);
      }
    });
  }

  override fieldDisplay(row: User, field: string): string {
    switch (field) {
      case 'id':
        return row.id?.toString() || '';
      case 'username':
        return row.username || '';
      case 'email':
        return row.email || '';
      case 'firstname':
        return row.firstname || '';
      case 'lastname':
        return row.lastname || '';
      case 'role':
        return row.role?.role || '';
      default:
        return '';
    }
  }
  
  override setPage(page: number, pageSize: number): void {
    let sortActive = '';
    let sortDirection = '';
    if (this.sorter) {
      sortActive = this.sorter.active;
      sortDirection = this.sorter.direction;
    }
    this.roleService.query('', page, pageSize, sortActive, sortDirection).subscribe({
      next: (data) => {
        this.observable.next(data);
      }
    });
  }
  
  override addRow(row: User): void {
    let page = 0;
    let pageSize = 100;
    if (this.paginator) {
      page = this.paginator.pageIndex;
      pageSize = this.paginator.pageSize;
    }
    this.roleService.create(row).subscribe({
      next: () => {
        this.setPage(page, pageSize);
      },
      error: (error) => {
        this.logger.error(`Error adding user: ${error}`);
      }
    });
  }
  
  override deleteRow(row: User): void {
    let page = 0;
    let pageSize = 100;
    if (this.paginator) {
      page = this.paginator.pageIndex;
      pageSize = this.paginator.pageSize;
    }
    if (row.id) {
      this.roleService.delete(row.id).subscribe({
        next: () => {
          this.setPage(page, pageSize);
        },
        error: (error) => {
          this.logger.error(`Error deleting user: ${error}`);
        }
      });
    }
  }
  
  override updateRow(row: User): void {
    let page = 0;
    let pageSize = 100;
    if (this.paginator) {
      page = this.paginator.pageIndex;
      pageSize = this.paginator.pageSize;
    }
    this.roleService.update(row).subscribe({
      next: () => {
        this.setPage(page, pageSize);
      },
      error: (error) => {
        this.logger.error(`Error updating user: ${error}`);
      }
    });
  }
  
  override async getTotalItemCount(): Promise<number> {
    return this.roleService.getTotalItemCount();
  }
  
}

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrl: './users.component.css',
  standalone: false
})
export class UsersComponent {
@ViewChild ('UserTable') table!: TableComponent<User>;
  dataSource: UserDataSource

  constructor(
    public dialog: MatDialog,
    logger: LoggerService,
    service: UserService) {
      this.dataSource = new UserDataSource(service, logger);
  }

  tableOptions: TableOptions = {
    sortable: true,
    pagable: true,
    pageSize: 5,
    searchable: true,
    tableActions: {
      selectRow: false,
      rowActions: [
        { icon: 'edit', event: 'editEvent'},
        { icon: 'cancel', event: 'deleteEvent' }
      ],
      addRow: true,
    },
    columns: [
      { name: 'ID', field: 'id', type: 'string', width: 50, sortable: false, hidden: true },
      { name: 'Firstname', field: 'firstname', type: 'string', width: 50, sortable: true, hidden: false },
      { name: 'Lastname', field: 'lastname', type: 'string', width: 50, sortable: true, hidden: false },
      { name: 'Username', field: 'username', type: 'string', width: 50, sortable: true, hidden: false },
      { name: 'Email', field: 'email', type: 'string', width: 50, sortable: true, hidden: false },
      { name: 'role', field: 'role', type: 'string', width: 50, sortable: true, hidden: false },
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
    } else {
      console.log('Unknown event action:', event.action);
    }
  }

  openEditDialog(row: Row): void {
    const dialogRef = this.dialog.open(AddEditUserDialogComponent, {
      width: '250px',
      height: '400px',
      data: { type: 'edit', user: row }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result !== null) {
        const user = result as User;
        if (user) {
          this.dataSource.updateRow(user);
        }
      }
    });
  }

  openAddDialog(): void {
    const dialogRef = this.dialog.open(AddEditUserDialogComponent, {
      width: '250px',
      height: '400px',
      data: { type: 'add', user: {} }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result !== null) {
        const user = result as User;
        if (user) {
          console.log('Adding user:', user);
          this.dataSource.addRow(user);
        }
      }
    });
  }

  openDeleteDialog(row: Row): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '250px',
      data: { message: `Are you sure you want to delete the user ${row['username']}?`}
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result === true) {
        const user = row as User;
        if (user) {
          this.dataSource.deleteRow(user);
        }
      }
    });
  }
}
