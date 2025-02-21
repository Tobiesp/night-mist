import { Injectable } from '@angular/core';
import { BaseDataService } from '../base-data.service';
import { Observable } from 'rxjs';

export interface Role {
  id: number;
  role: string;
  privileges: string[];
}

@Injectable({
  providedIn: 'root'
})
export class RoleService extends BaseDataService<Role> {
  TEST_ROLES: Role[] = [
    { id: 1, role: 'admin', privileges: ['Read', 'Write', 'Execute'] },
    { id: 2, role: 'user', privileges: ['Read'] },
    { id: 3, role: 'guest', privileges: ['Read'] },
    { id: 4, role: 'admin', privileges: ['Read', 'Write', 'Execute'] },
    { id: 5, role: 'user', privileges: ['Read'] },
    { id: 6, role: 'guest', privileges: ['Read'] },
    { id: 7, role: 'admin', privileges: ['Read', 'Write', 'Execute'] },
    { id: 8, role: 'user', privileges: ['Read'] },
    { id: 9, role: 'guest', privileges: ['Read'] },
    { id: 10, role: 'admin', privileges: ['Read', 'Write', 'Execute'] },
    { id: 11, role: 'user', privileges: ['Read'] },
    { id: 12, role: 'guest', privileges: ['Read'] },
  ];

  override getAll(): Observable<Role[]> {
    return new Observable<Array<Role>>(observer => {
      observer.next(this.TEST_ROLES);
      observer.complete();
    });
  }

  override get(id: number): Observable<Role> {
    return new Observable<Role>(observer => {
      observer.next(this.TEST_ROLES.find(r => r.id === id));
      observer.complete();
    });
  }
  
  override create(item: Role): Observable<Role> {
    item.id = this.TEST_ROLES.length + 1;
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
  
  override delete(id: number): Observable<Role> {
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
