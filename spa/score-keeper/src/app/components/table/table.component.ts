import { AfterViewInit, Component, EventEmitter, Input, OnInit, Output, ViewChild } from '@angular/core';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { MatSort, Sort, SortDirection } from '@angular/material/sort';
import { Observable, Subject } from 'rxjs';

export abstract class BaseDataSource<T extends Row> {

    observable: Subject<T[]> = new Subject<T[]>();
    activeSort: Sort = { active: '', direction: '' as SortDirection };
    protected paginator: MatPaginator | undefined;
    protected sorter: MatSort | undefined;
    protected pageSize: number = 25;

    abstract connect(): Observable<T[]>;
    abstract disconnect(): void;

    abstract filter(filterValue: string): void;
    abstract sortAction(sort: { active: string, direction: SortDirection }): void;

    abstract setPage(page: number, pageSize: number): void;

    abstract addRow(row: T): void;
    abstract deleteRow(row: T): void;
    abstract updateRow(row: T): void;
    abstract getTotalItemCount(): Promise<number>;

    abstract fieldDisplay(row: T, field: string): string;

    setPaginator(paginator: MatPaginator): void {
        this.paginator = paginator;
        if (this.paginator) {
            this.pageSize = this.paginator.pageSize;
            this.getTotalItemCount().then((count: number) => {
                this.paginator!.length = count;
            });
            this.paginator.page.subscribe((pageEvent: PageEvent) => {
                this.setPage(pageEvent.pageIndex, pageEvent.pageSize);
            }
        );
        }
    }

    setSort(sorter: MatSort): void {
        this.sorter = sorter;
        if (this.sorter) {
            this.sorter.sortChange.subscribe((sortEvent: Sort) => {
                this.sortAction({ active: sortEvent.active, direction: sortEvent.direction });
            });
        }
    }
}

export class ArrayDataSource<T extends Row> extends BaseDataSource<T> {
    viewData: T[] = [];
    constructor(private data: T[]) {
        super();
    }

    connect(): Observable<T[]> {
        this.observable.next(this.data);
        return this.observable;
    }

    disconnect(): void {}

    addRow(row: T): void {
        this.data.push(row);
        this.filter('');
    }

    deleteRow(row: T): void {
        const index = this.data.findIndex(r => r === row);
        if (index > -1) {
            this.data.splice(index, 1);
        }
        this.filter('');
    }

    updateRow(row: T): void {
        const index = this.data.findIndex(r => r['id'] === row['id']);
        if (index > -1) {
            this.data[index] = row;
        }
        this.filter('');
    }

    async getTotalItemCount(): Promise<number> {
        return Promise.resolve(this.data.length);
    }

    override fieldDisplay(row: T, field: string): string {
        const value = row[field];
        if (value instanceof Date) {
            return value.toLocaleDateString();
        }
        if (value instanceof Array) {
            return value.join(', ');
        }
        return value.toString();
    }

    override setPage(page: number, pageSize: number): void {
        const temp_data = this.viewData.slice(page * pageSize, (page + 1) * pageSize);
        this.observable.next(temp_data);
        if (this.paginator) {
            this.paginator.pageIndex = page;
        }
        if (this.sorter && this.sorter.active) {
            this.sortAction({ active: this.sorter.active, direction: this.sorter.direction });
        }
    }

    filter(filterValue: string): void {
        const fv = filterValue.trim().toLowerCase();
        this.viewData = this.data.filter(row => {
            return Object.keys(row).some(key => {
                return row[key].toString().toLowerCase().includes(fv);
            });
        });
        if (this.paginator) {
            this.setPage(0, this.paginator.pageSize);
        } else {
            if (this.sorter && this.sorter.active) {
                this.sortAction({ active: this.sorter.active, direction: this.sorter.direction });
            } else {
                this.observable.next(this.viewData);
            }
        }
    }

    sortAction(sort: { active: string, direction: SortDirection }): void {
        let temp_data = this.viewData;
        if (sort.active !== "" && sort.direction !== "") {
            this.activeSort = sort;
            temp_data = this.viewData.sort((a, b) => {
                if (sort.direction === 'asc') {
                    if (a[sort.active] < b[sort.active]) {
                        return -1;
                    }
                    if (a[sort.active] > b[sort.active]) {
                        return 1;
                    }
                    return 0;
                } else if (sort.direction === 'desc') {
                    if (a[sort.active] > b[sort.active]) {
                        return -1;
                    }
                    if (a[sort.active] < b[sort.active]) {
                        return 1;
                    }
                    return 0;
                } else {
                    return 0;
                }
            });
        }
        
        if (this.paginator) {
            const index = this.paginator.pageIndex
            const pageSize = this.paginator.pageSize;
            this.paginator.length = temp_data.length;
            const view_data = temp_data.slice(index * pageSize, (index + 1) * pageSize);
            this.observable.next(view_data);
        } else {
            this.observable.next(temp_data);
        }
    }
}

export interface columnDef {
    name: string;
    field: string;
    type: string;
    width: number;
    sortable: boolean;
    hidden: boolean;
}

export interface Row {
    [key: string]: any; // This allows indexing with a string
}

export interface eventAction {
    action: string;
    row: Row;
}

export interface RowOptions {
    title?: string;
    icon?: string;
    event: string;
}

export interface TableActions {
    selectRow?: boolean;
    rowActions: RowOptions[];
    addRow?: boolean;
}

export interface TableOptions {
    sortable: boolean;
    pagable: boolean;
    pageSize: number;
    searchable: boolean;
    tableActions: TableActions;
    columns: columnDef[];
}

@Component({
    selector: 'app-table',
    templateUrl: './table.component.html',
    styleUrl: './table.component.css',
    standalone: false
})
export class TableComponent<T extends Row> implements AfterViewInit {
    filterValue: string = '';
    protected data: T[] = [];

    @ViewChild(MatPaginator) paginator!: MatPaginator;
    @ViewChild(MatSort) sorter!: MatSort;

    @Input() config: TableOptions = {
        sortable: false,
        pagable: false,
        pageSize: 25,
        searchable: false,
        tableActions: {
            selectRow: false,
            rowActions: [],
            addRow: false
        },
        columns: []
    };
    @Input() dataSource: BaseDataSource<T> = new ArrayDataSource<T>([]);
    @Input() title: string = '';

    @Output() tableEvent = new EventEmitter<eventAction>()

    ngAfterViewInit(): void {
        this.dataSource.setPaginator(this.paginator);
        this.dataSource.setSort(this.sorter);
        this.dataSource.connect().subscribe({
            next: (data: T[]) => {
                this.data = data;
            }
        });
        this.dataSource.filter('');
    }

    handlePageEvent(event: PageEvent): void {
        console.log('Page event:', event);
    }

    applyFilter() {
        this.dataSource.filter(this.filterValue);
    }

    rowAction(action: string, row: Row): void {
        if (action === 'selectRowEvent' && !this.config.tableActions.selectRow) {
            return;
        }
        const eventData = {
            action: action,
            row: row
        };
        this.tableEvent.emit(eventData);
    }

    fieldDisplay(row: T, field: string): string {
        return this.dataSource.fieldDisplay(row, field);
    }

}
