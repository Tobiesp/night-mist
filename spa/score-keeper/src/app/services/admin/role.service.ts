import { Injectable } from '@angular/core';
import { BaseDataService } from '../base-data.service';
import { Observable } from 'rxjs';
import { Role } from '../auth.service';

@Injectable({
  providedIn: 'root'
})
export class RoleService extends BaseDataService<Role> {
  TEST_ROLES: Role[] = [
    { id: "1", role: 'admin', priviledges: [{name: 'admin', id: '1'}] },
    { id: "2", role: 'user1', priviledges: [{name: 'student_read', id: '1'}] },
    { id: "3", role: 'user2', priviledges: [{name: 'student_read', id: '1'}] },
    { id: "4", role: 'user3', priviledges: [{name: 'student_read', id: '1'}] },
    { id: "5", role: 'user4', priviledges: [{name: 'student_read', id: '1'}] },
    { id: "6", role: 'user5', priviledges: [{name: 'student_read', id: '1'}] },
    { id: "7", role: 'user6', priviledges: [{name: 'student_read', id: '1'}] },
    { id: "8", role: 'user7', priviledges: [{name: 'student_read', id: '1'}] },
    { id: "9", role: 'user8', priviledges: [{name: 'student_read', id: '1'}] },
    { id: "10", role: 'admin2', priviledges: [{name: 'admin', id: '1'}] },
    { id: "11", role: 'user9', priviledges: [{name: 'student_read', id: '1'}] },
    { id: "12", role: 'user10', priviledges: [{name: 'student_read', id: '1'}] },
  ];

  override getAll(): Observable<Role[]> {
    return new Observable<Array<Role>>(observer => {
      observer.next(this.TEST_ROLES);
      observer.complete();
    });
  }

  override get(id: string): Observable<Role> {
    return new Observable<Role>(observer => {
      observer.next(this.TEST_ROLES.find(r => r.id === id));
      observer.complete();
    });
  }
  
  override create(item: Role): Observable<Role> {
    item.id = (this.TEST_ROLES.length + 1).toString();
    this.TEST_ROLES.push(item);
    return new Observable<Role>(observer => {
      observer.next(item);
      observer.complete();
    });
  }
  
  override update(item: Role): Observable<Role> {
    const index = this.TEST_ROLES.findIndex(r => r.id === item.id);
    this.TEST_ROLES[index] = item;
    return new Observable<Role>(observer => {
      observer.next(item);
      observer.complete();
    });
  }
  
  override delete(id: string): Observable<Role> {
    const index = this.TEST_ROLES.findIndex(r => r.id === id);
    const role = this.TEST_ROLES[index];
    this.TEST_ROLES.splice(index, 1);
    return new Observable<Role>(observer => {
      observer.next(role);
      observer.complete();
    });
  }

  override query(filter_value: string, page: number, pageSize: number, sort_active: string, sort_direction: string): Observable<Role[]> {
    let data = this.TEST_ROLES;
    if (filter_value && filter_value.length > 0) {
      const fv = filter_value.toLowerCase();
      data = this.TEST_ROLES.filter(row => {
        return Object.keys(row).some((key: string) => {
            return (row[key as keyof Role] as unknown as string).toString().toLowerCase().includes(fv);
        });
      });
    }
    if (sort_active && sort_active !== "") {
      if (sort_direction === 'asc' || sort_direction === 'desc') {
        data.sort((a, b) => {
          if (a[sort_active as keyof Role] < b[sort_active as keyof Role]) {
            return sort_direction === 'asc' ? -1 : 1;
          }
          if (a[sort_active as keyof Role] > b[sort_active as keyof Role]) {
            return sort_direction === 'asc' ? 1 : -1;
          }
          return 0;
        });
      }
    }
    if (page >= 0 && pageSize > 0) {
      data = data.slice(page * pageSize, (page + 1) * pageSize);
    }
    return new Observable<Array<Role>>(observer => {
      observer.next(data);
      observer.complete();
    }
    );
  }

  override async getTotalItemCount(): Promise<number> {
    return new Promise<number>((resolve, reject) => {
      resolve(this.TEST_ROLES.length);
    });
  }
}
