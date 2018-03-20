<template>
  <form @submit.prevent="save">
    <div class="hero-body">
      <div class="container">
        <div class="columns is-vcentered">
          <div class="column is-6 is-offset-2">
            <h1 class="title">
              {{create_mode&&'Добаление хоста'||'Редактирование хоста'}}
            </h1>
            <div class="box">
              <div class="field">
                <label class="label">name</label>
                <div class="control">
                  <input class="input" v-model="host.name" type="text" autofocus required>
                </div>
              </div>
              <div class="field">
                <label class="label">ip</label>
                <div class="control">
                  <input class="input" v-model="host.ip" type="text">
                </div>
              </div>
              <div class="field">
                <label class="label">Открытые порты</label>
                <div class="control">
                  <input class="input" v-model="host.open_ports" type="text">
                </div>
              </div>
              <div class="field">
                <label class="label">group</label>
                <div class="control">
                  <v-select taggable push-tags v-model="host.group" :options="host._groups"></v-select>
                </div>
              </div>
              <div class="field">
                <label class="label">Comment</label>
                <div class="control">
                  <textarea class="textarea" v-model="host.comment"></textarea>
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
  name: 'host',
  metaInfo() { 
    return{
      title: this.create_mode?'Добавить хост':(this.host.name||'host')
    }
  },
  data () {
    return {
      host:{
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
      this.load_groups()
    }
  },
  methods: {
    load (id) {
      this.errors=null
      this.axios.get('/api/v1/hosts/'+id)
        .then((response) => {
          Vue.set(this,'host',response.data)
        },(error) => {
          this.errors = error
        })
    },
    load_groups () {
      this.axios.get('/api/v1/hosts/_groups')
        .then((response) => {
          Vue.set(this.host,'_groups',response.data)
        },(error) => {
          // this.errors = error
        })
    },
    save () {
      if(this.busy) return;
      this.errors=null;
      this.busy=true;
      (this.$route.params.id?
            this.axios.post('/api/v1/hosts/'+this.$route.params.id,this.host):
            this.axios.put('/api/v1/hosts',this.host))
        .then((response) => {
          this.$router.push('/hosts')
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
            that.axios.delete('/api/v1/hosts/'+that.$route.params.id)
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
        that.$router.push('/hosts')
      })
    }
  },
  components: {
    showerror
  }
}
</script>
