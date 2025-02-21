import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';

export interface iLogLevels {
  name: string;
  value: number;
}

export const LOG_LEVELS: iLogLevels[] = [
  { name: 'DEBUG', value: 1 },
  { name: 'INFO', value: 2 },
  { name: 'WARN', value: 3 },
  { name: 'ERROR', value: 4 },
];

@Injectable({
  providedIn: 'root'
})
export class LoggerService {

  constructor() { }

  info(message: string): void {
    this.log('INFO', message);
  }

  error(message: string): void {
    this.log('ERROR', message);
  }

  warn(message: string): void {
    this.log('WARN', message);
  }

  debug(message: string): void {
    this.log('DEBUG', message);
  }

  log(level: string, message: string): void {
    const logLevel = LOG_LEVELS.find(l => l.name === environment.logLevel);
    const levelObj = LOG_LEVELS.find(l => l.name === level);
    if (levelObj && logLevel && levelObj.value >= logLevel.value) {
      if (level === 'ERROR') {
        console.error(`${level}: ${message}`);
      }
      else if (level === 'WARN') {
        console.warn(`${level}: ${message}`);
      }
      else if (level === 'INFO') {
        console.info(`${level}: ${message}`);
      }
      else if (level === 'DEBUG') {
        if (!environment.production) {
          console.debug(`${level}: ${message}`);
        }
      }
      else {
        console.log(`${level}: ${message}`);
      }
    }
  }
}
