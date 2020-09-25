<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-row justify="center" align="center">
        <div class="display-2 font-weight-bold text-center">Flash Fiber Searcher</div>
      </v-row>
    </v-app-bar>
    <v-main>
      <main-searcher></main-searcher>
    </v-main>
  </v-app>
</template>

<script>

import MainSearcher from "./components/MainSearcher";

export default {
  name: 'App',

  components: {
    MainSearcher
  },

  data: () => ({
    //
  }),
};
</script>
