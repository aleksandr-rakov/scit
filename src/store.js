import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import auth_store from './modules/auth'

const store = new Vuex.Store({
  modules: {
    auth: auth_store,
  }
})

export default store;
