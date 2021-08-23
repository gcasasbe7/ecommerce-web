import { createStore } from 'vuex'

/* 
  Vuex > Application Global State Management
*/
export default createStore({
  /* State: Persist all the application data variables */
  state: {
    cart: {
      items: [],
    },
    isAuthenticated: false,
    authToken: '',
    isApplicationLoading: false,
  },

  /* Mutations: Define the data modifications as no direct editions are allowed */
  mutations: {
    initializeStore(state){
      if(localStorage.getItem('cart')) {
        state.cart = JSON.parse(localStorage.getItem('cart'))
      } else {
        localStorage.setItem('cart', JSON.stringify(state.cart))
      }
    },

    addToCart(state, item) {
      const exists = state.cart.items.filter(i => i.product.id === item.product.id)

      if(exists.length){
        exists[0].quantity = parseInt(exists[0].quantity) + parseInt(item.quantity)
      } else {
        state.cart.items.push(item)
      }

      localStorage.setItem('cart', JSON.stringify(state.cart))    
    },

    removeFromCart(state, item) {
      const index = this.state.cart.items.indexOf(item)
      if (index > -1) {
        this.state.cart.items.splice(index, 1);
      }

      localStorage.setItem('cart', JSON.stringify(state.cart))  
    },

    clearCart(state) {
      state.cart.items = []

      localStorage.setItem('cart', JSON.stringify(state.cart))    
    },

    setIsApplicationLoading(state, status) {
      this.state.isApplicationLoading = status
    }
  },

  /* Actions: Syncrhonized functions to modify the state data */
  actions: {
  },

  modules: {
  }
})
