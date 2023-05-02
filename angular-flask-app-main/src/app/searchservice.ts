import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SearchService {
  private readonly sendimg = 'http://127.0.0.1:5000/upsearch'; // 上传图片地址
  //上传图片会回调一个dbnet图片，所以不用请求了
  //请求crnn
  private readonly crnn = 'http://127.0.0.1:5000/getcrnn'; // crnn结果api
  //然后查询数据库
  private readonly database = 'http://127.0.0.1:5000/checkdb'; // 数据库api
  //查询openai
  private readonly openai = 'http://127.0.0.1:5000/openai';  // openai api

  constructor(private http: HttpClient) {}

  sendData(data: any): Observable<any> {
    // const headers = new HttpHeaders({
    //   'Content-Type': 'application/octet-stream'
    // });
    return this.http.post(this.sendimg, data,{observe: 'response', responseType: 'blob'});
  }

  fetchcrnn(): Observable<any> {
    return this.http.get(this.crnn,{observe: 'response', responseType: 'blob'});
  }

  fetchdb(): Observable<any> {
    return this.http.get(this.database,{observe: 'response', responseType: 'blob'});
  }

  fetchai(): Observable<any> {
    return this.http.get<any>(this.openai);
  }
}
