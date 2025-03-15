import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { BaseService } from './base.service';
import { HttpClient } from '@angular/common/http';
import { BaseModel } from '../models/models';

@Injectable({
  providedIn: 'root'
})
export abstract class AbstractDataService<T extends BaseModel> extends BaseService {

  constructor(public root_api:string, public client: HttpClient) {
    super();
  }

  /*
   * Abstract methods to get all the data.
   * Return an observable of the data.
   */
  getAll(): Observable<T[]>{
    return this.client.get<T[]>(this.baseUrl + '/' + this.root_api, { withCredentials: true });
  }

  /*
   * Abstract method to get a single item by id.
   * Return an observable of the data.
   */
  get(id: string): Observable<T> {
    return this.client.get<T>(this.baseUrl + '/' + this.root_api + '/' + id, { withCredentials: true });
  }
  
  /*
   * Abstract method to create a new item.
   * Return an observable of the data.
   */
  create(item: T): Observable<T> {
    return this.client.post<T>(this.baseUrl + '/' + this.root_api + '/', item, { withCredentials: true });
  }
  
  /*
   * Abstract method to update an item.
   * Return an observable of the data.
   */
  update(item: T): Observable<T> {
    return this.client.put<T>(this.baseUrl + '/' + this.root_api + '/' + item.id, item, { withCredentials: true });
  }
  
  /*
   * Abstract method to delete an item by id.
   * Return an observable of the data.
   */
  delete(id: string): Observable<T> {
    return this.client.delete<T>(this.baseUrl + '/' + this.root_api + '/' + id, { withCredentials: true });
  }
  
  /*
   * Abstract method to query the data.
   * Return an observable of the data
   */
  query(filter_value: string, page: number, pageSize: number, sort_active: string, sort_direction: string): Observable<T[]> {
    return this.client.get<T[]>(this.baseUrl + '/' + this.root_api + '/query?filter_value=' + filter_value + '&page_num=' + page + '&page_size=' + pageSize + '&sort_active=' + sort_active + '&sort_direction=' + sort_direction, { withCredentials: true });
  }

  /*
   * Abstract method to get the total items.
   * Return the number of total items.
   */
  getTotalItemCount(): Observable<number> {
    return this.client.get<number>(this.baseUrl + '/' + this.root_api + '/count', { withCredentials: true });
  } 

}
