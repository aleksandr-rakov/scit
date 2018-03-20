<template>
  <form @submit.prevent="save">
    <div class="hero-body">
      <div class="container">
        <div class="columns is-vcentered">
          <div class="column is-6 is-offset-2">
            <h1 class="title">
              {{create_mode&&'Добаление приложение'||'Редактирование приложения'}}
            </h1>
            <div class="box">
              <div class="field">
                <label class="label">name</label>
                <div class="control">
                  <input class="input" v-model="app.name" type="text" autofocus required>
                </div>
              </div>
              <div class="field">
                <label class="label">token</label>
                <div class="control">
                  <input class="input" v-model="app.token" type="text">
                </div>
              </div>

              <div class="field is-grouped">
                <div class="control">
                  <button class="button is-primary" :class="{'is-loading':busy}">Сохранить</button>
                </div>
                <div class="control">
                  <button class="button is-warning" @click.prevent="remove" v-show="!create_mode">Удалить</button>
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
  name: 'app',
  metaInfo() { 
    return{
      title: this.create_mode?'Добавить приложение':(this.app.name||'app')
    }
  },
  data () {
    return {
      app:{
      },
      busy: false,
      errors: null,
      create_mode: false,
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
      this.axios.get('/api/v1/apps/'+id)
        .then((response) => {
          Vue.set(this,'app',response.data)
        },(error) => {
          this.errors = error
        })
    },
    save () {
      if(this.busy) return;
      this.errors=null;
      this.busy=true;
      (this.$route.params.id?
            this.axios.post('/api/v1/apps/'+this.$route.params.id,this.app):
            this.axios.put('/api/v1/apps',this.app))
        .then((response) => {
          this.$router.push('/apps')
          this.busy=false
        },(error) => {
          this.errors=error
          this.busy=false
        })
    },
    remove(){
      var that=this;
      this.$swal({
        title: 'Точно удаить ?',
        showCancelButton: true,
        confirmButtonText: 'Удалить',
        cancelButtonText: 'Отмена',
        showLoaderOnConfirm: true,
        preConfirm: function (password) {
          return new Promise(function (resolve, reject) {
            that.axios.delete('/api/v1/apps/'+that.$route.params.id)
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
        that.$router.push('/apps')
      })
    }
  },
  components: {
    showerror
  }
}
</script>
