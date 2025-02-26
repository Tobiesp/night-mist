import { Component, Injectable, ViewChild } from '@angular/core';
import { BaseDataSource, Row, TableComponent, TableOptions } from '../../../components/table/table.component';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../../components/confirm-dialog/confirm-dialog.component';
import { AddEditRoleDialogComponent } from './add-edit-role-dialog/add-edit-role-dialog.component';
import { RoleService } from '../../../services/admin/role.service';
import { Observable } from 'rxjs';
import { LoggerService } from '../../../services/logger.service';
import { Role } from '../../../services/auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class RoleDataSource extends BaseDataSource<Role> {
  dataview: Role[] = [];
  constructor(
    private roleService: RoleService, 
    public logger: LoggerService
  ) {
    super();
  }

  override connect(): Observable<Role[]> {
    let pageSize = 100;
    if (this.paginator) {
      pageSize = this.paginator.pageSize
    }
    this.roleService.query('', 0, pageSize, '', '').subscribe({
      next: (data) => {
        this.observable.next(data);
      },
      error: (error) => {
        this.logger.error(`Error loading roles: ${error}`);
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
        this.logger.error(`Error filtering roles: ${error}`);
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
    this.logger.debug(`Sort roles: ${sort.active} ${sort.direction}`);
    this.roleService.query('', page, pageSize, sort.active, sort.direction).subscribe({
      next: (data) => {
        this.observable.next(data);
      },
      error: (error) => {
        this.logger.error(`Error sort roles: ${error}`);
      }
    });
  }

  override fieldDisplay(row: Role, field: string): string {
    switch (field) {
      case 'id':
        return row.id.toString();
      case 'role':
        return row.role;
      case 'privileges':
        const names = row.priviledges.map(priviledge => priviledge.name);
        return names.join(', ');
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
  
  override addRow(row: Role): void {
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
        this.logger.error(`Error adding role: ${error}`);
      }
    });
  }
  
  override deleteRow(row: Role): void {
    let page = 0;
    let pageSize = 100;
    if (this.paginator) {
      page = this.paginator.pageIndex;
      pageSize = this.paginator.pageSize;
    }
    this.roleService.delete(row.id).subscribe({
      next: () => {
        this.setPage(page, pageSize);
      },
      error: (error) => {
        this.logger.error(`Error deleting role: ${error}`);
      }
    });
  }
  
  override updateRow(row: Role): void {
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
        this.logger.error(`Error updating role: ${error}`);
      }
    });
  }
  
  override async getTotalItemCount(): Promise<number> {
    return this.roleService.getTotalItemCount();
  }
  
}

@Component({
  selector: 'app-roles',
  templateUrl: './roles.component.html',
  styleUrl: './roles.component.css',
  standalone: false
})
export class RolesComponent {
  @ViewChild ('RoleTable') table!: TableComponent<Role>;
  dataSource: RoleDataSource

  constructor(
    public dialog: MatDialog,
    logger: LoggerService,
    roleService: RoleService) {
      this.dataSource = new RoleDataSource(roleService, logger);
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
      { name: 'ID', field: 'id', type: 'number', width: 50, sortable: false, hidden: true },
      { name: 'Name', field: 'role', type: 'string', width: 50, sortable: true, hidden: false },
      { name: 'Privileges', field: 'privileges', type: 'string', width: 150, sortable: false, hidden: false }
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
    const dialogRef = this.dialog.open(AddEditRoleDialogComponent, {
      width: '250px',
      height: '400px',
      data: { type: 'edit', role: row }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result !== null) {
        const role = result as Role;
        if (role) {
          this.dataSource.updateRow(role);
        }
      }
    });
  }

  openAddDialog(): void {
    const dialogRef = this.dialog.open(AddEditRoleDialogComponent, {
      width: '250px',
      height: '400px',
      data: { type: 'add', role: {} }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result !== null) {
        const role = result as Role;
        if (role) {
          console.log('Adding role:', role);
          this.dataSource.addRow(role);
        }
      }
    });
  }

  openDeleteDialog(row: Row): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '250px',
      data: { message: `Are you sure you want to delete the role ${row['role']}?`}
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result === true) {
        const role = row as Role;
        if (role) {
          this.dataSource.deleteRow(role);
        }
      }
    });
  }
}
