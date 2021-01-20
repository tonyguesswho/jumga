import Vue from 'vue';
import Chakra, { CThemeProvider, CReset } from '@chakra-ui/vue';
import App from './App.vue';
// import store from './store';
import router from './router';
import axios from 'axios';
import VueNoty from "vuejs-noty";
import "vuejs-noty/dist/vuejs-noty.css";


// axios.defaults.withCredentials = true
axios.defaults.baseURL = 'https://jumga-tony.herokuapp.com/api/';

// axios.interceptors.response.use(undefined, function (error) {
//   if (error) {
//     const originalRequest = error.config;
//     if (error.response.status === 401 && !originalRequest._retry) {

//       originalRequest._retry = true;
//       store.dispatch('LogOut')
//       return router.push('/login')
//     }
//   }
// })
Vue.use(VueNoty, {
  timeout: 4000,
  progressBar: true,
  layout: "topCenter"
});
Vue.use(Chakra)
Vue.config.productionTip = false;
const userData = localStorage.getItem("user");
const sellerData = localStorage.getItem("seller");
const saccountData = localStorage.getItem("account");


new Vue({
  router,
  data: {
    user: userData ? JSON.parse(userData) : null,
    seller: sellerData ? JSON.parse(sellerData) : null
  },
  el: '#app',
  render: (h) => h(CThemeProvider, [h(CReset), h(App)])
}).$mount()

