<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <h2 @click="addToCart">Add to cart</h2>
    <h2 @click="clearCart">Clear cart</h2>
    <h2 v-bind:class="{'is-loading' : $store.state.isApplicationLoading}">IS LOADING?</h2>
    <p>
      For a guide and recipes on how to configure / customize this project,<br>
      check out the
      <a href="https://cli.vuejs.org" target="_blank" rel="noopener">vue-cli documentation</a>.
    </p>
    <h3>Installed CLI Plugins</h3>
    <ul>
      <li><a href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-babel" target="_blank" rel="noopener">babel</a></li>
      <li><a href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-router" target="_blank" rel="noopener">router</a></li>
      <li><a href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-vuex" target="_blank" rel="noopener">vuex</a></li>
    </ul>
    <h3>Essential Links</h3>
    <ul>
      <li><a href="https://vuejs.org" target="_blank" rel="noopener">Core Docs</a></li>
      <li><a href="https://forum.vuejs.org" target="_blank" rel="noopener">Forum</a></li>
      <li><a href="https://chat.vuejs.org" target="_blank" rel="noopener">Community Chat</a></li>
      <li><a href="https://twitter.com/vuejs" target="_blank" rel="noopener">Twitter</a></li>
      <li><a href="https://news.vuejs.org" target="_blank" rel="noopener">News</a></li>
    </ul>
    <h3>Ecosystem</h3>
    <ul>
      <li><a href="https://router.vuejs.org" target="_blank" rel="noopener">vue-router</a></li>
      <li><a href="https://vuex.vuejs.org" target="_blank" rel="noopener">vuex</a></li>
      <li><a href="https://github.com/vuejs/vue-devtools#vue-devtools" target="_blank" rel="noopener">vue-devtools</a></li>
      <li><a href="https://vue-loader.vuejs.org" target="_blank" rel="noopener">vue-loader</a></li>
      <li><a href="https://github.com/vuejs/awesome-vue" target="_blank" rel="noopener">awesome-vue</a></li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

export default {  
  name: 'HelloWorld',
  props: {
    msg: String
  },
  mounted() {
    document.title = "Hola | iPadel"
  },
  methods: {
    addToCart() {
      // Todo check we have a valid quantity to add to the basket
      
      // Build the item object to be added to the basket
      const item = {
        product: {
          "id": 2,
          "name": "BullPadel Vertex 2",
        },
        quantity: 3
      }

      this.$store.commit('addToCart', item)

      this.$store.commit('setIsApplicationLoading', !this.$store.state.isApplicationLoading)
    },
    clearCart() {
      this.$store.commit('clearCart')
    },

    // Needs to be an async method to trigger in linear order the code lines and display the 
    // loading screen correctly
    async exampleLoading() {
      // Assert we are loading the content
      this.$store.commit('setIsApplicationLoading', true)

      // Do heavy stuff... Await keyword to block the code runtime and wait for the asyncronous task to finish
      await axios
        .get('/api/v1/all-products')
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.log(error)
        })

      // Assert we are loading the content
      this.$store.commit('setIsApplicationLoading', true)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.is-loading {
  color: #ff0000;
}
</style>
