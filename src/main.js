import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueSweetAlert from 'vue-sweetalert'
import Meta from 'vue-meta'
import VueSelect from 'vue-select'

// Require the main Sass manifest file
require('./assets/main.scss');

// Add a request interceptor
axios.interceptors.request.use(function (config) {
    // Do something before request is sent
    config.headers['X-Token'] = localStorage.getItem('user');
    return config;
  }, function (error) {
    // Do something with request error
    return Promise.reject(error);
  });

Vue.use(VueSweetAlert)
Vue.use(VueAxios, axios)
Vue.use(Meta)
Vue.component('v-select', VueSelect)


Vue.config.productionTip = false

new Vue({
  render: h => h(App)
}).$mount('#app')
