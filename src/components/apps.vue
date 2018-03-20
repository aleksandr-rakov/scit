<template lang="html">
  <div>
    <h1 class="title">
      <router-link class="button is-active is-pulled-right" :to="{ path: '/apps/add'}">
        Создать приложение
      </router-link>
      Хосты
    </h1>

    <showerror :error="errors"></showerror>

    <div v-for="app in apps">
      <router-link :to="{ path: '/apps/'+app._id}">
        {{app.name}}
      </router-link>
    </div>

  </div>
</template>

<script>
import showerror from "./showerror"

export default {
  name: 'apps',
  metaInfo: {
    title: 'apps'
  },
  data: function () {
    return {
      apps: [],
      errors: ''
    }
  },
  methods: {
    loadapps: function () {
      this.errors=null
      this.axios.get('/api/v1/apps').then((response) => {
        this.apps=response.data;
      }, (err) => {
        this.errors=err;
      })
    }
  },
  mounted: function () {
    this.loadapps()
  },
  components:{
    showerror
  }
}
</script>

<style>

</style>
