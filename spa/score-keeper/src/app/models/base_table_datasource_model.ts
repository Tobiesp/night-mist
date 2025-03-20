import { Observable } from "rxjs";
import { BaseDataSource } from "../components/table/table.component";
import { AbstractDataService } from "../services/abstract-data.service";
import { LoggerService } from "../services/logger.service";
import { BaseModel } from "./models";

export abstract class BaseTableDataSourceModel<T extends BaseModel> extends BaseDataSource<T> {

    public DEFAULT_PAGE_SIZE = 100;
    public DEFAULT_PAGE = 0;

    constructor(
        private service: AbstractDataService<T>, 
        public logger: LoggerService
    ) {
        super();
    }

    override connect(): Observable<T[]> {
        let pageSize = this.DEFAULT_PAGE_SIZE;
        if (this.paginator) {
          pageSize = this.paginator.pageSize
        }
        this.service.query('', this.DEFAULT_PAGE, pageSize, '', '').subscribe({
          next: (data) => {
            this.observable.next(data);
          },
          error: (error) => {
            throw new Error(`Error loading ${this.service.root_api}: ${error.error.error}`, error.status);
          }
        });
        return this.observable;
      }
    
      override disconnect(): void {
        this.observable.complete();
      }
      
      override filter(filterValue: string): void {
        const page = this.DEFAULT_PAGE;
        let pageSize = this.DEFAULT_PAGE_SIZE;
        if (this.paginator) {
          pageSize = this.paginator.pageSize;
        }
        let sortActive = '';
        let sortDirection = '';
        if (this.sorter) {
          sortActive = this.sorter.active;
          sortDirection = this.sorter.direction;
        }
        this.service.query(filterValue, page, pageSize, sortActive, sortDirection).subscribe({
          next: (data) => {
            this.observable.next(data);
          },
          error: (error) => {
            throw new Error(`Error filtering ${this.service.root_api}: ${error.error.error}`, error.status);
          }
        });
      }
      
      override sortAction(sort: { active: string; direction: string; }): void {
        let page = this.DEFAULT_PAGE;
        let pageSize = this.DEFAULT_PAGE_SIZE;
        if (this.paginator) {
          page = this.paginator.pageIndex;
          pageSize = this.paginator.pageSize;
        }
        this.logger.debug(`Sort roles: ${sort.active} ${sort.direction}`);
        this.service.query('', page, pageSize, sort.active, sort.direction).subscribe({
          next: (data) => {
            this.observable.next(data);
          },
          error: (error) => {
            throw new Error(`Error sorting ${this.service.root_api}: ${error.error.error}`, error.status);
          }
        });
      }
      
      override setPage(page: number, pageSize: number): void {
        let sortActive = '';
        let sortDirection = '';
        if (this.sorter) {
          sortActive = this.sorter.active;
          sortDirection = this.sorter.direction;
        }
        this.service.query('', page, pageSize, sortActive, sortDirection).subscribe({
          next: (data) => {
            this.observable.next(data);
          },
          error: (error) => {
            throw new Error(`Error getting page ${page} for ${this.service.root_api}: ${error.error.error}`, error.status);
          }
        });
      }
      
      override addRow(row: T): void {
        let page = this.DEFAULT_PAGE;
        let pageSize = this.DEFAULT_PAGE_SIZE;
        if (this.paginator) {
          page = this.paginator.pageIndex;
          pageSize = this.paginator.pageSize;
        }
        this.service.create(row).subscribe({
          next: () => {
            this.setPage(page, pageSize);
          },
          error: (error) => {
            throw new Error(`Error adding role: ${error.error.error}`, error.status);
          }
        });
      }
      
      override deleteRow(row: T): void {
        let page = this.DEFAULT_PAGE;
        let pageSize = this.DEFAULT_PAGE_SIZE;
        if (this.paginator) {
          page = this.paginator.pageIndex;
          pageSize = this.paginator.pageSize;
        }
        if (!row.id) {
          return;
        }
        this.service.delete(row.id).subscribe({
          next: () => {
            this.setPage(page, pageSize);
          },
          error: (error) => {
            throw new Error(`Error deleting role: ${error.error.error}`, error.status);
          }
        });
      }
      
      override updateRow(row: T): void {
        let page = this.DEFAULT_PAGE;
        let pageSize = this.DEFAULT_PAGE_SIZE;
        if (this.paginator) {
          page = this.paginator.pageIndex;
          pageSize = this.paginator.pageSize;
        }
        this.service.update(row).subscribe({
          next: () => {
            this.setPage(page, pageSize);
          },
          error: (error) => {
            throw new Error(`Error updating role: ${error.error.error}`, error.status);
          }
        });
      }
      
      override async getTotalItemCount(): Promise<number> {
        const count = await this.service.getTotalItemCount().toPromise();
        return count ?? 0;
      }

}