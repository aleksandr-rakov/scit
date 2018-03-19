<template lang="html">
  <div>
    <h1 class="title">
      <router-link class="button is-active is-pulled-right" :to="{ path: '/hosts/add'}">
        Создать хост
      </router-link>
      Хосты
    </h1>

    <showerror :error="errors"></showerror>

    <div class="hosts-group" v-for="group in hosts">
      <h2>{{group.name||'Нет'}}</h2>
      <div class="hosts-host" v-for="host in group.hosts">
        <router-link :to="{ path: '/hosts/'+host._id}">
          {{host.name}}
        </router-link>
        {{host.ip}}

        <span v-show="host.open_ports">
          : {{host.open_ports}}
        </span>

        <div class="host-comment">{{host.comment}}</div>
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
  margin-left: 10px;
}
.hosts-host{
  margin-left: 15px;
  margin-bottom: 15px;
}
</style>
