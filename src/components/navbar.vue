<template lang="html">
  <nav class="navbar">
    <div class="navbar-menu">
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
          <a class="button" @click.prevent="logout" v-show="profile">
            Выйти
          </a>
          <router-link class="button" :to="{ path: '/login/'}" v-show="!profile">
            Войти
          </router-link>
        </span>
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
    }
  },
  methods: {
    logout () {
      auth.logout()
    }
  },
  computed: {
    ...mapState({
      profile: state => state.auth.profile
    })
  }
}
</script>
