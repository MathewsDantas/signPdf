import axios from "axios";
// import Cookies from "js-cookie";

export const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

// api.interceptors.request.use(
//   (config) => {
//     const token = Cookies.get("token");

//     if (token) {
//       config.headers.Authorization = `Bearer ${token}`;
//     } else {
//       delete config.headers.Authorization;
//     }
//     return config;
//   },
//   async (error) => await Promise.reject(error)
// );

// Este comentário não deve acionar a pipeline
