import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class MessagesService {

  massages: string[]=[];

  add(massages:string){
    this.massages.push(massages)
  }
  clear(){
    this.massages=[]
  }

  constructor() { }
}
