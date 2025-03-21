import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AbstractDataService } from '../abstract-data.service';
import { Event, EventInstance } from '../../models/models';
import { LoggerService } from '../logger.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EventsService extends AbstractDataService<Event>{

  constructor(private logger: LoggerService, client: HttpClient) {
      super('events', client);
    }
    
    /*
      * Get a new event instance unless the last event instance is still open then return that.
      * Return an observable of the data.
      */
    startNewInstance(event: Event): Observable<EventInstance>{
      return this.client.post<EventInstance>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instance', { withCredentials: true });
    }

    /* Get the last event instance
     * Return an observable of the data.
     */
    getLastInstance(event: Event): Observable<EventInstance>{
      return this.client.get<EventInstance>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instance/last', { withCredentials: true });
    }

    /* Get a specific event instance
     * Return an observable of the data.
     */
    getInstance(event: Event, eventInstance: EventInstance): Observable<EventInstance>{
      return this.client.get<EventInstance>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instance/' + eventInstance.id, { withCredentials: true });
    }

    /* Mark an event as complete 
     * Return an observable of the data.
     */
    completeEvent(event: Event): Observable<Event>{
      return this.client.post<Event>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/complete', {}, { withCredentials: true });
    }

    /* Mark an event instance as complete
     * Return an observable of the data.
     */
    completeInstance(event: Event, instance: EventInstance): Observable<EventInstance>{
      return this.client.post<EventInstance>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instance/' + instance.id + '/complete', {}, { withCredentials: true });
    }

    /* Get all event instances
     * Return an observable of the data.
     */
    getAllEventInstances(event: Event): Observable<EventInstance[]>{
      return this.client.get<EventInstance[]>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instances', { withCredentials: true });
    }

    /* Get count of all event instances
     * Return an observable of the data.
     */
    getInstanceCount(event: Event): Observable<number>{
      return this.client.get<number>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instances/count', { withCredentials: true });
    }

    /* Delete an event instance
     */
    deleteInstance(event: Event, instance: EventInstance): Observable<void>{
      return this.client.delete<void>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instance/' + instance.id, { withCredentials: true });
    }

    /* Purge all event instances
     */
    purgeInstances(event: Event): Observable<void>{
      return this.client.delete<void>(this.baseUrl + '/' + this.root_api + '/' + event.id + '/instances/purge', { withCredentials: true });
    }
    
}
