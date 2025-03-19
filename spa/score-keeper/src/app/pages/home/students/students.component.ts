import { Component, Injectable, ViewChild } from '@angular/core';
import { BaseTableDataSourceModel } from '../../../models/base_table_datasource_model';
import { Student } from '../../../models/models';
import { LoggerService } from '../../../services/logger.service';
import { StudentsService } from '../../../services/students/students.service';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../../components/confirm-dialog/confirm-dialog.component';
import { TableComponent, TableOptions, Row } from '../../../components/table/table.component';
import { AddEditRoleDialogComponent } from '../../admin-pages/roles/add-edit-role-dialog/add-edit-role-dialog.component';
import { AddEditStudentDialogComponent } from './add-edit-student-dialog/add-edit-student-dialog.component';

@Injectable({
  providedIn: 'root'
})
export class StudentDataSource extends BaseTableDataSourceModel<Student> {
  constructor(
    private studentService: StudentsService, 
    logger: LoggerService
  ) {
    super(studentService, logger);
  }

  override fieldDisplay(row: Student, field: string): string {
    switch (field) {
      case 'id':
        return row.id || '';
      case 'firstname':
        return row.firstname || '';
        case 'lastname':
          return row.lastname || '';
      case 'grade':
        return row.grade?.grade_name || '';
        case 'student_group':
          return row.student_group?.group_name || '';
      default:
        return '';
    }
  }
  
}

@Component({
  selector: 'app-students',
  templateUrl: './students.component.html',
  styleUrl: './students.component.css',
  standalone: false
})
export class StudentsComponent {
  @ViewChild ('StudentTable') table!: TableComponent<Student>;
  dataSource: StudentDataSource

  constructor(
    public dialog: MatDialog,
    private logger: LoggerService,
    studentsService: StudentsService) {
      this.dataSource = new StudentDataSource(studentsService, logger);
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
      { name: 'Firstname', field: 'firstname', type: 'string', width: 50, sortable: true, hidden: false },
      { name: 'Lastname', field: 'lastname', type: 'string', width: 150, sortable: false, hidden: false },
      { name: 'Grade', field: 'grade', type: 'string', width: 150, sortable: false, hidden: false },
      { name: 'Group', field: 'student_group', type: 'string', width: 150, sortable: false, hidden: false }
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
      this.logger.error(`Unknown event action: ${event.action}`);
    }
  }

  openEditDialog(row: Row): void {
    const dialogRef = this.dialog.open(AddEditStudentDialogComponent, {
      width: '250px',
      height: '450px',
      data: { type: 'edit', role: row }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result !== null && result !== undefined) {
        const student = result as Student;
        if (student) {
          this.dataSource.updateRow(student);
        }
      }
    });
  }

  openAddDialog(): void {
    const dialogRef = this.dialog.open(AddEditStudentDialogComponent, {
      width: '250px',
      height: '450px',
      data: { type: 'add', role: {} }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result !== null) {
        const student = result as Student;
        if (student) {
          this.dataSource.addRow(student);
        }
      }
    });
  }

  openDeleteDialog(row: Row): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '250px',
      data: { message: `Are you sure you want to delete the student ${row['firstname']} ${row['lastname']}?`}
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result === true) {
        const student = row as Student;
        if (student) {
          this.dataSource.deleteRow(student);
        }
      }
    });
  }

}
