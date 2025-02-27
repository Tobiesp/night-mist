import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminComponent } from './pages/admin-pages/admin/admin.component';
import { LoginComponent } from './pages/login-pages/login/login.component';
import { HomeComponent } from './pages/home/home.component';
import { PageNotFound } from './pages/page-not-found-component/page-not-found-component.component';
import { AuthGuard } from './guards/auth.guard';
import { AccessDeniedPageComponent } from './pages/access-denied-page/access-denied-page.component';
import { PointsEarnedComponent } from './pages/points-earned/points-earned.component';
import { PointsSpentComponent } from './pages/points-spent/points-spent.component';
import { ReporterComponent } from './pages/reporter/reporter.component';
import { EventsComponent } from './pages/events/events.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'admin', component: AdminComponent, canActivate: [AuthGuard], data: { priviledges: ['admin'] } },
  { path: 'home', component: HomeComponent, canActivate: [AuthGuard], data: { priviledges: ['student_read'] } },
  { path: 'points-earned', component: PointsEarnedComponent, canActivate: [AuthGuard], data: { priviledges: ['student_read'] } },
  { path: 'points-spent', component: PointsSpentComponent, canActivate: [AuthGuard], data: { priviledges: ['student_read'] } },
  { path: 'events', component: EventsComponent, canActivate: [AuthGuard], data: { priviledges: ['student_read'] } },
  { path: 'reporter', component: ReporterComponent, canActivate: [AuthGuard], data: { priviledges: ['student_read'] } },
  { path: '403', component: AccessDeniedPageComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' },  // redirect to `home`
  { path: '**', component: PageNotFound}
];

export { routes };

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }