import {MessagesService} from './messages.service';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {Hero} from './hero';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})




export class HeroService {
  constructor(private massagesServers: MessagesService, private HttpClient:HttpClient) { }
   heroesList:any=[]
   ratinglist:any=[]
  getHero(id: string): Observable<Hero> {
    const hero= this.HttpClient.get<Hero>('http://127.0.0.1:5000/detail/'+ id.toString())
    console.log(hero)
    this.massagesServers.add('hero ID number ' + id.toString()+' is fetch')
    return hero;
  }

  localHeroes(): Observable<Hero[]>{
    return this.heroesList;
  }

  getHeroes(): Observable<Hero[]>{
    console.log('Server on')
    const heroes= this.HttpClient.get<Hero[]>('http://127.0.0.1:5000/')
    this.heroesList=heroes
    this.massagesServers.add('The hero server is on')
    return this.heroesList;
  }

  getrationgs(): Observable<Hero[]>{
    console.log('rating')
    this.ratinglist= this.HttpClient.get<Hero[]>('http://127.0.0.1:5000/rating')
    return this.ratinglist;
  }

  updateHero(hero: Hero): Observable<Hero>{
    console.log(hero)
    return this.HttpClient.post<Hero>('http://127.0.0.1:5000/update',hero)
  }

  addHero(obj:any): Observable<Hero>{
    console.log('start serve')
    console.log(obj)
    return this.HttpClient.post<Hero>('http://127.0.0.1:5000/add', obj)
  }

  delbook(id:string): Observable<Hero> {
    let url='http://127.0.0.1:5000/delbook/'+id
    const res = this.HttpClient.get<Hero>('http://127.0.0.1:5000/delbook/' + id)
    console.log(url)
    return res
  }
}
