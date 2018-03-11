<template>
  <form @submit.prevent="login">
    <div class="hero-body">
      <div class="container">
        <div class="columns is-vcentered">
          <div class="column is-4 is-offset-4">
            <h1 class="title">
              Авторизация
            </h1>
            <div class="box">
              <div class="field">
                <label class="label">Логин</label>
                <div class="control">
                  <input class="input" v-model="email" type="text" autofocus required>
                </div>
              </div>
              <div class="field">
                <label class="label">Пароль</label>
                <div class="control">
                  <input class="input" v-model="password" type="password" required>
                </div>
              </div>
              <div class="field is-grouped">
                <div class="control">
                  <button class="button is-primary" :class="{'is-loading':busy}">Войти</button>
                </div>
              </div>
            </div>
            <showerror :error="errors"></showerror>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
import auth  from '../auth'
import showerror from "./showerror"

export default {
  name: 'login',
  metaInfo: {
    title: 'Авторизация'
  },
  data () {
    return {
      email: '',
      password: '',
      errors: '',
      busy: false,
    }
  },
  methods: {
    login () {
      if(this.busy) return;
      this.errors=null
      this.busy=true;
      auth.login(this, {login:this.email, password:this.password},'/hosts').then(() => {
        // Reset the password so that the next login will have this field empty.
        this.password = ''
        this.busy=false;
      },() =>{
        this.busy=false;
      })
    }
  },
  components: {
    showerror
  }
}
</script>
