<template lang="html">
  <div>
    <h1 class="title">
      <router-link class="button is-active is-pulled-right" :to="{ path: '/hosts/add'}">
        Создать хост
      </router-link>
      Хосты
    </h1>

    <showerror :error="errors"></showerror>

    <div class="columns" v-for="group in hosts">
      <div class="column">
        <h2>{{group.name||'Нет'}}</h2>
        <div class="group-level">
          <div class="columns" v-for="host in group.hosts">
            <div class="column">
              <router-link :to="{ path: '/hosts/'+host._id}">
                {{host.name}}
              </router-link>
              {{host.ip}}
              <div class="host-comment">{{host.comment}}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import showerror from "./showerror"

export default {
  name: 'hosts',
  metaInfo: {
    title: 'Hosts'
  },
  data: function () {
    return {
      hosts: [],
      errors: ''
    }
  },
  methods: {
    loadHosts: function () {
      this.errors=null
      this.axios.get('/api/v1/hosts/by_group').then((response) => {
        this.hosts=response.data;
      }, (err) => {
        this.errors=err;
      })
    }
  },
  mounted: function () {
    this.loadHosts()
  },
  components:{
    showerror
  }
}
</script>

<style>
.host-comment{
  white-space: pre-wrap;
  font-size: 12px;
  line-height: 12px;  
}
.group-level{
  padding-left: 15px;
}
</style>
