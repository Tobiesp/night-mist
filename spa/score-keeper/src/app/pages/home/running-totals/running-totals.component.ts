import { Component, Injectable, ViewChild } from '@angular/core';
import { BaseTableDataSourceModel } from '../../../models/base_table_datasource_model';
import { RunningTotal } from '../../../models/models';
import { LoggerService } from '../../../services/logger.service';
import { RunningTotalsService } from '../../../services/points/running-totals.service';
import { MatDialog } from '@angular/material/dialog';
import { TableComponent, TableOptions } from '../../../components/table/table.component';


@Injectable({
  providedIn: 'root'
})
export class TotalDataSource extends BaseTableDataSourceModel<RunningTotal> {
  constructor(
    private totalsService: RunningTotalsService, 
    logger: LoggerService
  ) {
    super(totalsService, logger);
  }

  override fieldDisplay(row: RunningTotal, field: string): string {
    switch (field) {
      case 'id':
        return row.id || '';
      case 'student':
        return row.student.firstname + ' ' + row.student.lastname;
      case 'total_points':
        return row.total_points.toString();
      default:
        return '';
    }
  }
  
}

@Component({
  selector: 'app-running-totals',
  templateUrl: './running-totals.component.html',
  styleUrl: './running-totals.component.css',
  standalone: false
})
export class RunningTotalsComponent {
  @ViewChild ('RunningTotalTable') table!: TableComponent<RunningTotal>;
    dataSource: TotalDataSource
  
    constructor(
      public dialog: MatDialog,
      logger: LoggerService,
      totalsService: RunningTotalsService) {
        this.dataSource = new TotalDataSource(totalsService, logger);
    }
  
    tableOptions: TableOptions = {
      sortable: true,
      pagable: true,
      pageSize: 15,
      searchable: true,
      tableActions: {
        selectRow: false,
        rowActions: [],
        addRow: false,
      },
      columns: [
        { name: 'ID', field: 'id', type: 'number', width: 50, sortable: false, hidden: true },
        { name: 'Student', field: 'student', type: 'string', width: 50, sortable: true, hidden: false },
        { name: 'Total Points', field: 'total_points', type: 'string', width: 150, sortable: false, hidden: false }
      ]
    };

}
