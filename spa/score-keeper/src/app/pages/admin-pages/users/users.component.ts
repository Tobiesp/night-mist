import { Component, Injectable, ViewChild } from '@angular/core';
import { Observable } from 'rxjs';
import { BaseDataSource, Row, TableComponent, TableOptions } from '../../../components/table/table.component';
import { UserService } from '../../../services/admin/user.service';
import { LoggerService } from '../../../services/logger.service';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../../components/confirm-dialog/confirm-dialog.component';
import { AddEditUserDialogComponent } from './add-edit-user-dialog/add-edit-user-dialog/add-edit-user-dialog.component';
import { User } from '../../../models/models';
import { BaseTableDataSourceModel } from '../../../models/base_table_datasource_model';

@Injectable({
  providedIn: 'root'
})
export class UserDataSource extends BaseTableDataSourceModel<User> {
  constructor(
    private userService: UserService, 
    logger: LoggerService
  ) {
    super(userService, logger);
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
        return row.role?.role_name || '';
      case 'account_locked':
        return row.account_locked ? 'Locked' : 'Active';
      case 'last_login':
        const date_str = row.last_login;
        if (date_str) {
          const date = new Date(date_str);
          return date.toLocaleString();
        }
        return '';
      default:
        return '';
    }
  }

  lockUser(user: User): void {
    this.userService.lockUser(user).subscribe({
      next: (data: any) => {
        
      },
      error: (error: any) => {
        throw new Error(`Error locking user: ${error}`);
      }
    });
  }

  unlockUser(user: User): void {
    this.userService.unlockUser(user).subscribe({
      next: (data: any) => {
        
      },
      error: (error: any) => {
        throw new Error(`Error unlocking user: ${error}`);
      }
    });
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
        { icon: 'lock', event: 'lockEvent'},
        { icon: 'edit', event: 'editEvent'},
        { icon: 'delete', event: 'deleteEvent' }
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
      { name: 'Account Locked', field: 'account_locked', type: 'string', width: 50, sortable: true, hidden: false },
      { name: 'Last Login', field: 'last_login', type: 'string', width: 50, sortable: true, hidden: false },
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
    } else if (event.action === 'lockEvent') {
      if (event.row.account_locked) {
        this.openUnlockDialog(event.row);
      } else {
        this.openLockDialog(event.row);
      }
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
        const user = result as User;
        if (user) {
          this.dataSource.updateRow(user);
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

  openLockDialog(row: Row): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '250px',
      data: { message: `Are you sure you want to lock the user ${row['username']}?`}
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result === true) {
        const user = row as User;
        if (user) {
          this.dataSource.lockUser(user);
        }
      }
    });
  }

  openUnlockDialog(row: Row): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '250px',
      data: { message: `Are you sure you want to unlock the user ${row['username']}?`}
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result === true) {
        const user = row as User;
        if (user) {
          this.dataSource.unlockUser(user);
        }
      }
    });
  }
}
