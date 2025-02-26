import { Injectable } from '@angular/core';
import { User } from '../auth/auth.service';
import { BaseDataService } from '../base-data.service';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService extends BaseDataService<User> {
  TEST_USERS: User[] = [
    { id: "1", username: 'admin', firstname: 'Admin', lastname: 'Admin', email: 'testadmin@email.com', role: { id: "1", role: 'admin_role', priviledges: [{ name: 'admin', id: '1' }] } },
    { id: "2", username: 'user1', firstname: 'User', lastname: 'One', email: 'test@email.com', role: { id: "2", role: 'user_role', priviledges: [{ name: 'student_read', id: '1' }] } },
    { id: "3", username: 'user2', firstname: 'User', lastname: 'Two', email: 'test@email.com', role: { id: "2", role: 'user_role', priviledges: [{ name: 'student_read', id: '1' }] } },
    { id: "4", username: 'user3', firstname: 'User', lastname: 'Three', email: 'test@email.com', role: { id: "2", role: 'user_role', priviledges: [{ name: 'student_read', id: '1' }] } },
    { id: "5", username: 'user4', firstname: 'User', lastname: 'Four', email: 'test@email.com', role: { id: "2", role: 'user_role', priviledges: [{ name: 'student_read', id: '1' }] } },
    { id: "6", username: 'user5', firstname: 'User', lastname: 'Five', email: 'test@email.com', role: { id: "2", role: 'user_role', priviledges: [{ name: 'student_read', id: '1' }] } },
    { id: "7", username: 'user6', firstname: 'User', lastname: 'Six', email: 'test@email.com', role: { id: "2", role: 'user_role', priviledges: [{ name: 'student_read', id: '1' }] } },
  ];
  
    override getAll(): Observable<User[]> {
      return new Observable<Array<User>>(observer => {
        observer.next(this.TEST_USERS);
        observer.complete();
      });
    }
  
    override get(id: string): Observable<User> {
      return new Observable<User>(observer => {
        observer.next(this.TEST_USERS.find(r => r.id === id));
        observer.complete();
      });
    }
    
    override create(item: User): Observable<User> {
      item.id = (this.TEST_USERS.length + 1).toString();
      this.TEST_USERS.push(item);
      return new Observable<User>(observer => {
        observer.next(item);
        observer.complete();
      });
    }
    
    override update(item: User): Observable<User> {
      const index = this.TEST_USERS.findIndex(r => r.id === item.id);
      this.TEST_USERS[index] = item;
      return new Observable<User>(observer => {
        observer.next(item);
        observer.complete();
      });
    }
    
    override delete(id: string): Observable<User> {
      const index = this.TEST_USERS.findIndex(r => r.id === id);
      const role = this.TEST_USERS[index];
      this.TEST_USERS.splice(index, 1);
      return new Observable<User>(observer => {
        observer.next(role);
        observer.complete();
      });
    }
    
      override query(filter_value: string, page: number, pageSize: number, sort_active: string, sort_direction: string): Observable<User[]> {
        let data = this.TEST_USERS;
        if (filter_value && filter_value.length > 0) {
          const fv = filter_value.toLowerCase();
          data = this.TEST_USERS.filter(row => {
            return Object.keys(row).some((key: string) => {
                return (row[key as keyof User] as unknown as string).toString().toLowerCase().includes(fv);
            });
          });
        }
        if (sort_active && sort_active !== "") {
          if (sort_direction === 'asc' || sort_direction === 'desc') {
            data.sort((a, b) => {
              const aValue = a[sort_active as keyof User];
              const bValue = b[sort_active as keyof User];

              if (aValue === undefined || bValue === undefined) {
                if (aValue === undefined && bValue !== undefined) {
                  return sort_direction === 'asc' ? -1 : 1;
                }
                if (aValue !== undefined && bValue === undefined) {
                  return sort_direction === 'asc' ? 1 : -1;
                }
                return 0;
              }
              if (aValue !== undefined && bValue !== undefined) {
                if (aValue < bValue) {
                  return sort_direction === 'asc' ? -1 : 1;
                }
                if (aValue > bValue) {
                  return sort_direction === 'asc' ? 1 : -1;
                }
                return 0;
              }
              return 0;
            });
          }
        }
        if (page >= 0 && pageSize > 0) {
          data = data.slice(page * pageSize, (page + 1) * pageSize);
        }
        return new Observable<Array<User>>(observer => {
          observer.next(data);
          observer.complete();
        }
        );
      }
    
      override async getTotalItemCount(): Promise<number> {
        return new Promise<number>((resolve, reject) => {
          resolve(this.TEST_USERS.length);
        });
      }
}
