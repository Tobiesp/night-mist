import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AbstractDataService } from '../abstract-data.service';
import { PointEvent, EventInstance } from '../../models/models';
import { LoggerService } from '../logger.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EventsService extends AbstractDataService<PointEvent>{

  constructor(private logger: LoggerService, client: HttpClient) {
      super('events', client);
    }
    
    /*
      * Get a new event instance unless the last event instance is still open then return that.
      * Return an observable of the data.
      */
    startNewInstance(event: PointEvent): Observable<EventInstance>{
      return this.client.post<EventInstance>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instance', { withCredentials: true });
    }

    /* Get the last event instance
     * Return an observable of the data.
     */
    getLastInstance(event: PointEvent): Observable<EventInstance>{
      return this.client.get<EventInstance>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instance/last', { withCredentials: true });
    }

    /* Get a specific event instance
     * Return an observable of the data.
     */
    getInstance(event: PointEvent, eventInstance: EventInstance): Observable<EventInstance>{
      return this.client.get<EventInstance>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instance/' + eventInstance.id, { withCredentials: true });
    }

    /* Mark an event as complete 
     * Return an observable of the data.
     */
    completeEvent(event: PointEvent): Observable<PointEvent>{
      return this.client.post<PointEvent>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/complete', {}, { withCredentials: true });
    }

    /* Mark an event instance as complete
     * Return an observable of the data.
     */
    completeInstance(event: PointEvent, instance: EventInstance): Observable<EventInstance>{
      return this.client.post<EventInstance>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instance/' + instance.id + '/complete', {}, { withCredentials: true });
    }

    /* Get all event instances
     * Return an observable of the data.
     */
    getAllEventInstances(event: PointEvent): Observable<EventInstance[]>{
      return this.client.get<EventInstance[]>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instances', { withCredentials: true });
    }

    /* Get count of all event instances
     * Return an observable of the data.
     */
    getInstanceCount(event: PointEvent): Observable<number>{
      return this.client.get<number>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instances/count', { withCredentials: true });
    }

    /* Delete an event instance
     */
    deleteInstance(event: PointEvent, instance: EventInstance): Observable<void>{
      return this.client.delete<void>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instance/' + instance.id, { withCredentials: true });
    }

    /* Purge all event instances
     */
    purgeInstances(event: PointEvent): Observable<void>{
      return this.client.delete<void>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instances/purge', { withCredentials: true });
    }
    
}
