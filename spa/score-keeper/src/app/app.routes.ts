import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminComponent } from './pages/admin-pages/admin/admin.component';
import { LoginComponent } from './pages/login/login.component';
import { HomeComponent } from './pages/home/home.component';
import { PageNotFound } from './pages/page-not-found-component/page-not-found-component.component';
import { AuthGuard } from './guards/auth.guard';
import { RolesComponent } from './pages/admin-pages/roles/roles.component';
import { UsersComponent } from './pages/admin-pages/users/users.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'admin', component: AdminComponent, canActivate: [AuthGuard], data: { priviledges: ['admin'] } },
  { path: 'admin/roles', component: RolesComponent, canActivate: [AuthGuard], data: { priviledges: ['admin'] } },
  { path: 'admin/users', component: UsersComponent, canActivate: [AuthGuard], data: { priviledges: ['admin'] } },
  { path: 'home', component: HomeComponent, canActivate: [AuthGuard], data: { priviledges: ['student_read'] } },
  { path: '', redirectTo: '/home', pathMatch: 'full' },  // redirect to `home`
  { path: '**', component: PageNotFound}
];

export { routes };

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }