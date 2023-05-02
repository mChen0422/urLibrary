import { DashboardComponent } from './dashboard/dashboard.component';
import { MessagesComponent } from './messages/messages.component';
import { HeroDetailesComponent } from './hero-detailes/hero-detailes.component';
import { HeroesComponent } from './heroes/heroes.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {AddoneComponent} from "./addone/addone.component";
import {SearchComponent} from "./search/search.component";


const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'top-list', component: HeroesComponent },
  { path: 'home', component: DashboardComponent},
  { path: 'book_detail/:_id' , component: HeroDetailesComponent},
  { path: 'addone' , component: AddoneComponent},
  { path: 'search' , component: SearchComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
