import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { LoggerService } from './logger.service';

@Injectable({
  providedIn: 'root'
})
export class BaseServiceService{
  protected baseUrl = environment.baseUrl;
}
