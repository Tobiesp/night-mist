import { Injectable } from '@angular/core';
import { LoggerService } from './logger.service';
import { Observable } from 'rxjs';
import { BaseServiceService } from './base-service.service';

@Injectable({
  providedIn: 'root'
})
export abstract class BaseDataService<T> extends BaseServiceService {

  /*
   * Abstract methods to get all the data.
   * Return an observable of the data.
   */
  abstract getAll(): Observable<T[]>;

  /*
   * Abstract method to get a single item by id.
   * Return an observable of the data.
   */
  abstract get(id: number): Observable<T>;
  
  /*
   * Abstract method to create a new item.
   * Return an observable of the data.
   */
  abstract create(item: T): Observable<T>;
  
  /*
   * Abstract method to update an item.
   * Return an observable of the data.
   */
  abstract update(item: T): Observable<T>;
  
  /*
   * Abstract method to delete an item by id.
   * Return an observable of the data.
   */
  abstract delete(id: number): Observable<T>;
  
  /*
   * Abstract method to query the data.
   * Return an observable of the data
   */
  abstract query(filter_value: string, page: number, pageSize: number, sort_active: string, sort_direction: string): Observable<T[]>;

  /*
   * Abstract method to get the total items.
   * Return the number of total items.
   */
  abstract getTotalItemCount(): Promise<number>;
}
