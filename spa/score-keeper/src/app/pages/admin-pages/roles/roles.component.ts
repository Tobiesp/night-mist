import { Component, Injectable, ViewChild } from '@angular/core';
import { Row, TableComponent, TableOptions } from '../../../components/table/table.component';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../../components/confirm-dialog/confirm-dialog.component';
import { AddEditRoleDialogComponent } from './add-edit-role-dialog/add-edit-role-dialog.component';
import { RoleService } from '../../../services/admin/role.service';
import { LoggerService } from '../../../services/logger.service';
import { Priviledge, Role } from '../../../models/models';
import { BaseTableDataSourceModel } from '../../../models/base_table_datasource_model';

@Injectable({
  providedIn: 'root'
})
export class RoleDataSource extends BaseTableDataSourceModel<Role> {
  constructor(
    private roleService: RoleService, 
    logger: LoggerService
  ) {
    super(roleService, logger);
  }

  override fieldDisplay(row: Role, field: string): string {
    switch (field) {
      case 'id':
        return row.id || '';
      case 'role_name':
        return row.role_name;
      case 'priviledges':
        const names = row.priviledges.map((priviledge: Priviledge) => priviledge.priviledge_name);
        return names.join(', ');
      default:
        return '';
    }
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
      { name: 'Name', field: 'role_name', type: 'string', width: 50, sortable: true, hidden: false },
      { name: 'Priviledges', field: 'priviledges', type: 'string', width: 150, sortable: false, hidden: false }
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
      data: { message: `Are you sure you want to delete the role ${row['role_name']}?`}
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
