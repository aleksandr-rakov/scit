<template lang="html">
  <nav class="navbar">
    <div class="container">
      <div class="navbar-burger burger" @click.prevent="toggle" :class="{'is-active':toggled}">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <div class="navbar-menu" :class="{'is-active':toggled}">
        <div class="navbar-start">
          <router-link class="navbar-item is-brand" to="/">
            Vue Project
          </router-link>
          <router-link class="navbar-item is-tab" to="/hosts">
            Хосты
          </router-link>
          <router-link class="navbar-item is-tab" to="/users">
            Пользователи
          </router-link>
        </div>
        <div class="navbar-end">
          <span class="navbar-item">
            {{profile&&profile.name||''}}
          </span>
          <span class="navbar-item">
            <a class="button" @click.prevent="logout" v-show="profile">
              Выйти
            </a>
            <router-link class="button" :to="{ path: '/login/'}" v-show="!profile">
              Войти
            </router-link>
          </span>
        </div>
      </div>
    </div>  
  </nav>
</template>

<script>
import auth  from '../auth'
import { mapState } from 'vuex'

export default {
  name: 'navbar',
  data: function () {
    return {
      toggled: false,
    }
  },
  methods: {
    logout () {
      auth.logout()
    },
    toggle () {
      this.toggled=!this.toggled
    }
  },
  computed: {
    ...mapState({
      profile: state => state.auth.profile
    })
  }
}
</script>
