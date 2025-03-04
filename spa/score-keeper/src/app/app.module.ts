import { CUSTOM_ELEMENTS_SCHEMA, NgModule, provideZoneChangeDetection } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule, routes } from './app.routes';
import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';
import { AdminComponent } from './pages/admin-pages/admin/admin.component';
import { LoginComponent } from './pages/login-pages/login/login.component';
import { provideRouter, RouterOutlet } from '@angular/router';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule, MatLabel } from '@angular/material/form-field';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HeadingComponent } from './components/heading/heading.component';
import { CommonModule } from '@angular/common';
import { SnackbarComponent } from './components/snackbar/snackbar.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { TableComponent } from './components/table/table.component';
import { RolesComponent } from './pages/admin-pages/roles/roles.component';
import { MatDialogModule } from '@angular/material/dialog';
import { ConfirmDialogComponent } from './components/confirm-dialog/confirm-dialog.component';
import { AddEditRoleDialogComponent } from './pages/admin-pages/roles/add-edit-role-dialog/add-edit-role-dialog.component';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatMenuModule } from '@angular/material/menu';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MenuHeaderComponent } from './components/menu-header/menu-header.component';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { MatTabsModule } from '@angular/material/tabs';
import { UsersComponent } from './pages/admin-pages/users/users.component';
import { PointsEarnedComponent } from './pages/points-earned/points-earned.component';
import { PointsSpentComponent } from './pages/points-spent/points-spent.component';
import { ReporterComponent } from './pages/reporter/reporter.component';
import { EventsComponent } from './pages/events/events.component';
import { AccessDeniedPageComponent } from './pages/access-denied-page/access-denied-page.component';
import { PageNotFound } from './pages/page-not-found-component/page-not-found-component.component';
import { ForgotPasswordDialogComponent } from './pages/login-pages/forgot-password-dialog/forgot-password-dialog.component';
import { SignupDialogComponent } from './pages/login-pages/signup-dialog/signup-dialog.component';
import { AddEditUserDialogComponent } from './pages/admin-pages/users/add-edit-user-dialog/add-edit-user-dialog/add-edit-user-dialog.component';

@NgModule({
    declarations: [
        AppComponent,
        AdminComponent,
        UsersComponent,
        RolesComponent,
        HomeComponent,
        PointsEarnedComponent,
        PointsSpentComponent,
        ReporterComponent,
        EventsComponent,
        LoginComponent,
        AccessDeniedPageComponent,
        PageNotFound,
        HeadingComponent,
        SnackbarComponent,
        TableComponent,
        ConfirmDialogComponent,
        AddEditRoleDialogComponent,
        MenuHeaderComponent,
        ForgotPasswordDialogComponent,
        SignupDialogComponent,
        AddEditUserDialogComponent,
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        MatInputModule,
        MatButtonModule,
        MatCardModule,
        MatFormFieldModule,
        RouterOutlet,
        BrowserAnimationsModule,
        CommonModule,
        ReactiveFormsModule,
        FormsModule,
        MatDialogModule,
        MatSelectModule,
        MatChipsModule,
        MatAutocompleteModule,
        MatIconModule,
        MatToolbarModule,
        MatMenuModule,
        MatIconModule,
        MatSidenavModule,
        MatPaginatorModule,
        MatTableModule,
        MatSortModule,
        MatTabsModule,
    ],
    providers: [provideZoneChangeDetection({ eventCoalescing: true }), provideRouter(routes)],
    bootstrap: [AppComponent],
    schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AppModule { }