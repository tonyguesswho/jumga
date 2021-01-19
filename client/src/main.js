import Vue from 'vue';
import Chakra, { CThemeProvider, CReset } from '@chakra-ui/vue';
import App from './App.vue';
import store from './store';
import router from './router';
import axios from 'axios';


axios.defaults.withCredentials = true
axios.defaults.baseURL = 'https://jumga-tony.herokuapp.com/api';

axios.interceptors.response.use(undefined, function (error) {
  if (error) {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {

      originalRequest._retry = true;
      store.dispatch('LogOut')
      return router.push('/login')
    }
  }
})

Vue.use(Chakra)

new Vue({
  store,
  router,
  el: '#app',
  render: (h) => h(CThemeProvider, [h(CReset), h(App)])
}).$mount()