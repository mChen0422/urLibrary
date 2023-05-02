import { HeroService } from '../hero.service';
import { Component, OnInit } from '@angular/core';
import { Hero } from '../hero';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})

export class DashboardComponent implements OnInit {

  heroes: Hero[]=[];

  x:number=Math.floor(Math.random() * 10);
  constructor(private HeroService:HeroService) { }

  ngOnInit(): void {
    this.getHeroes()
    console.log(this.heroes)
  }

  getHeroes():void{
    this.HeroService.getHeroes()
    .subscribe(heroes=> this.heroes=heroes.slice(this.x,this.x+18))

  }

}
