import axios from 'axios'
import config from '../config'

const baseUrl = process.env.NODE_ENV === 'development' ? config.baseUrl.dev : config.baseUrl.pro
console.log("baseUrl:",baseUrl)

export function uploadPicturessApi(data) {
  return axios({
    url: "https://jsonplaceholder.typicode.com/posts/", // 请求地址
    method: "post",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    data,
  });
}