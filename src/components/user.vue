<template>
  <form @submit.prevent="save">
    <div class="hero-body">
      <div class="container">
        <div class="columns is-vcentered">
          <div class="column is-6 is-offset-2">
            <h1 class="title">
              {{create_mode&&'Добаление пользователя'||'Редактирование пользователя'}}
            </h1>
            <div class="box">
              <div class="field">
                <label class="label">name</label>
                <div class="control">
                  <input class="input" v-model="user.name" type="text" autofocus required>
                </div>
              </div>
              <div class="field">
                <label class="label">login</label>
                <div class="control">
                  <input class="input" v-model="user.login" type="text" required>
                </div>
              </div>
              <div class="field" v-if="create_mode">
                <label class="label">Password</label>
                <div class="control">
                  <input class="input" v-model="user.password" type="password" required>
                </div>
              </div>

              <div class="field">
                <div class="control">
                  <label class="checkbox">
                    <input class="checkbox" v-model="user.disabled" type="checkbox">
                    disabled
                  </label>
                </div>
              </div>

              <div class="field is-grouped">
                <div class="control">
                  <button class="button is-primary" :class="{'is-loading':busy}">Сохранить</button>
                </div>
                <div class="control">
                  <button class="button is-warning" @click.prevent="change_password" v-show="!create_mode">Изменить пароль</button>
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
import Vue from "vue"
import showerror from "./showerror"

export default {
  name: 'user',
  metaInfo() { 
    return{
      title: this.create_mode?'Добавить пользователя':(this.user.name||'User')
    }
  },
  data () {
    return {
      user:{
        name: '',
        login: '',
        password: '',
        disabled: false,
      },
      busy: false,
      errors: null,
      create_mode: false
    }
  },
  mounted: function () {
    if(this.$route.params.id){
      this.load(this.$route.params.id)
    }else{
      this.create_mode=true
    }
  },
  methods: {
    load (id) {
      this.errors=null
      this.axios.get('/api/v1/users/'+id)
        .then((response) => {
          Vue.set(this,'user',response.data)
        },(error) => {
          this.errors = error
        })
    },
    save () {
      if(this.busy) return;
      this.errors=null;
      this.busy=true;
      (this.$route.params.id?
            this.axios.post('/api/v1/users/'+this.$route.params.id,this.user):
            this.axios.put('/api/v1/users',this.user))
        .then((response) => {
          this.$router.push('/users')
          this.busy=false
        },(error) => {
          this.errors=error
          this.busy=false
        })
    },
    change_password(){
      var that=this;
      this.$swal({
        title: 'Введите новый пароль',
        input: 'text',
        showCancelButton: true,
        confirmButtonText: 'Изменить',
        cancelButtonText: 'Отмена',
        showLoaderOnConfirm: true,
        preConfirm: function (password) {
          return new Promise(function (resolve, reject) {
            that.axios.post('/api/v1/users/'+that.$route.params.id+'/change_password',{password})
              .then(function(response) {
                resolve()
              },function(error){
                if(error.response && error.response.data.errors){
                  reject(JSON.stringify(error.response.data.errors,null,' '))
                }else{
                  reject(error)
                }
              })
          })
        },
        allowOutsideClick: false
      }).then(function (confirmed) {
        that.$swal({
          type: 'success',
          title: 'Готово!',
          html: 'Пароль изменен'
        })
      })
    }
  },
  components: {
    showerror
  }
}
</script>
