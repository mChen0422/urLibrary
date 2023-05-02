import { MessagesService } from './../messages.service';
import { Component, OnInit } from '@angular/core';
import { Hero } from '../hero';
import { HeroService } from '../hero.service';
import { Router } from '@angular/router';
import {toNumbers} from "@angular/compiler-cli/src/version_helpers";
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { SearchService} from "../searchservice";
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css'],
})
export class SearchComponent implements OnInit {
  imageUrl: any;
  showresult: boolean = false;
  dbimg:any ="assets/loading.gif";
  loadimg:any = "assets/loading.gif";
  rcnnimg:any = "assets/loading.gif";
  databaseimg:any="assets/loading.gif";
  aiimg:any="assets/loading.gif";
  ailoading:any = true;
  aidone:any=false;
  aitext:any=''
  constructor(private myService: SearchService, private sanitizer: DomSanitizer) {}
  onFileSelected(event: any) {

    const file: File = event.target.files[0];
    const reader = new FileReader();

    if (file.type !== 'image/jpeg') {
      alert('仅支持 JPG 格式的图片！');

    }else{
      this.showresult = true;
      reader.onload = (event: any) => {
        this.imageUrl = event.target.result;
        // console.log(this.imageUrl)
      }
      reader.readAsDataURL(file);

      const formData = new FormData();
      formData.append('file', file);
      this.myService.sendData(formData).subscribe((response) => {
        // console.log(response)
        const reader = new FileReader();
        reader.readAsDataURL(response.body);
        reader.onloadend = () => {
          this.dbimg = reader.result as string;
        };
        this.myService.fetchcrnn().subscribe((response) => {
          // console.log(response)
          const reader2 = new FileReader();
          reader2.readAsDataURL(response.body);
          reader2.onloadend = () => {
            this.rcnnimg = reader2.result as string;
          };
          this.myService.fetchdb().subscribe((response) => {
            // console.log(response)
            const reader3 = new FileReader();
            reader3.readAsDataURL(response.body);
            reader3.onloadend = () => {
              this.databaseimg = reader3.result as string;
            }
            this.myService.fetchai().subscribe((response) => {
              console.log(response.text)
              this.ailoading = false;
              this.aidone = true;
              this.aitext = response.text;

            });
          });
        })
      });
    }
  }


  ngOnInit() {
  }

}
