import { FormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeroesComponent } from './heroes/heroes.component';
import { HeroDetailesComponent } from './hero-detailes/hero-detailes.component';
import { MessagesComponent } from './messages/messages.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import {SafePipeModule } from 'safe-pipe';
import {AddoneComponent} from "./addone/addone.component";

import {SearchComponent} from "./search/search.component";


@NgModule({
  declarations: [
    AppComponent,
    HeroesComponent,
    HeroDetailesComponent,
    MessagesComponent,
    DashboardComponent,
    AddoneComponent,
    SearchComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    SafePipeModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {


}
