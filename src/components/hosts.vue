<template lang="html">
  <div>
    <h1 class="title">
      <router-link class="button is-active is-pulled-right" :to="{ path: '/hosts/add'}">
        Создать хост
      </router-link>
      Хосты
    </h1>

    <showerror :error="errors"></showerror>

    <div class="columns" v-for="host in hosts">
      <div class="column">
        <router-link :to="{ path: '/hosts/'+host._id}" v-bind:class="{host_disabled:host.disabled}">
          {{host.name}}
        </router-link>
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
      this.axios.get('/api/v1/hosts').then((response) => {
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
.host_disabled{
  color: #ccc;
}
</style>
