import { MessagesService } from './../messages.service';
import { Component, OnInit } from '@angular/core';
import { Hero } from '../hero';
import { HeroService } from '../hero.service';
import { Router } from '@angular/router';
import {toNumbers} from "@angular/compiler-cli/src/version_helpers";

@Component({
  selector: 'app-addone',
  templateUrl: './addone.component.html',
  styleUrls: ['./addone.component.css']
})
export class AddoneComponent implements OnInit {

heroes: Hero[]=[];
ratinglist:Hero[]=[];

  constructor (private router: Router,private heroService:HeroService, private messagesServicer:MessagesService) { }

  ngOnInit(): void {
    this.heroService.getrationgs().subscribe(ratinglist => {this.ratinglist = ratinglist.slice(0,10)});
    // console.log('??')
  }

  getHeroes(): void{
    this.heroService.getHeroes().subscribe(heroes => {this.heroes = heroes})
    console.log("i'm on")

  }


  add(isbn: string,title : string,auth: string,year : string,pub: string,urls : string,rating : string, count : string):void{
    console.log('start process')
    const score:any = Number(rating.trim())*Number(count.trim())
    var dataobj={
      'ISBN':isbn.trim(),
      'Book_Title':title.trim(),
      'Book_Author':auth.trim(),
      'Year_Of_Publication':year.trim(),
      'Publisher':pub.trim(),
      'Image_URL_S':urls.trim(),
      'Image_URL_M':urls.trim(),
      'Image_URL_L':urls.trim(),
      'rating':rating.trim(),
      'score':score,
      'count':count.trim()
    }
    console.log(dataobj)
    this.heroService.addHero( dataobj).subscribe(h=>{this.heroes.push(h)})
    this.heroService.getHeroes().subscribe(heroes=> this.heroes=heroes)
    this.router.navigate(['/'])


  }

}
