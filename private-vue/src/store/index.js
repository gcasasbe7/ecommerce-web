import { createStore } from 'vuex'
import storageHelper from '@/helpers/storage_helper.js'
/* 
  Vuex > Application Global State Management
*/

export default createStore({
  /* State: Persist all the application data variables */
  state: {
    user: {
      tokens: {
        access_token: '',
        refresh_token: ''
      },
      email: '',
      name: '',
      surname: ''
    },
    cart: {
      items: [],
      creation_date: '',
    },
    isApplicationLoading: false,
    previousPath: '',
  },

  /* Mutations: Define the data modifications as no direct editions are allowed */
  mutations: {
    initializeStore(state){
      // Attempt to initialize the cart
      if(localStorage.getItem('cart')) {
        state.cart = JSON.parse(localStorage.getItem('cart'))
      } else {
        localStorage.setItem('cart', JSON.stringify(state.cart))
      }

      // Attempt to initialize the user
      if(storageHelper.getUser()) {
        // Init the user
        state.user = storageHelper.getUser()
        // Assert it's logged in
        helpers.onLoginUser(state, state.user)
      }
    },

    addToCart(state, item) {
      if(state.cart.creation_date.length == 0){
        state.cart.creation_date = new Date().toLocaleString();
      }
      
      const exists = state.cart.items.filter(i => i.product.id === item.product.id)

      if(exists.length){
        exists[0].quantity = parseInt(exists[0].quantity) + parseInt(item.quantity)
      } else {
        state.cart.items.push(item)
      }

      localStorage.setItem('cart', JSON.stringify(state.cart))    
    },

    removeFromCart(state, item) {
      const index = state.cart.items.indexOf(item)
      if (index > -1) {
        state.cart.items.splice(index, 1);
      }

      if (state.cart.items.length == 0) {
        state.cart.creation_date = ''
      }

      localStorage.setItem('cart', JSON.stringify(state.cart))  
    },

    clearCart(state) {
      state.cart.items = []
      state.cart.creation_date = ''

      localStorage.setItem('cart', JSON.stringify(state.cart))    
    },

    setIsApplicationLoading(state, status) {
      state.isApplicationLoading = status
    },

    onLoginUser(state, data) {
      helpers.onLoginUser(state, data)
    },

    onLogoutUser(state) {
      helpers.onLogoutUser(state)
    },

    setUserAccessToken(state, access_token) {
      state.user.tokens.access_token = access_token
      storageHelper.storeUser(state.user)
    }
  },

  /* Actions: Syncrhonized functions to modify the state data */
  actions: {},
  modules: {},
  
  /* Define store getters */
  getters: {
    get_formatted_cart: state => {
      let f_cart = []
      state.cart.items.forEach(element => {
        f_cart.push({
          "product_id": element.product.id,
          "quantity": element.quantity
        })
      })
      return f_cart
    },
    is_user_logged_in: state => {
      // Build a list with the required parameters to determine if we currently have a user session
      let data = [state.user.tokens.access_token, state.user.tokens.refresh_token, state.user.name, state.user.surname, state.user.email]
      // Iterate the list to validate the values
      for(let i = 0; i < data.length; i++) {if(!data[i]){return false}}
      return true
    },
    get_user_object: state => {return state.user},
    get_user_name: state => {return state.user.name},
    get_full_user_name: state => {return `${state.user.name} ${state.user.surname}`},
    get_user_email: state => {return state.user.email}
  }
})

const helpers = {
  onLoginUser: (state, data) => {
    // Bind the user data
    state.user.name = data.name
    state.user.surname = data.surname
    state.user.email = data.email
    state.user.tokens.access_token = data.tokens.access_token
    state.user.tokens.refresh_token = data.tokens.refresh_token
    // storageHelper.setCookie(storageHelper.ACCESS_TOKEN_KEY, data.tokens.access_token)
    // Store the user into the local Storage (Along with his refresh token)
    storageHelper.storeUser(state.user)
  },
  onLogoutUser: (state) => {
    // Reset the store User data structure
    state.user = {
      tokens: {
        access_token: '',
        refresh_token: ''
      },
      email: '',
      name: '',
      surname: ''
    }
    // Remove the user object from the local storage
    storageHelper.removeUser()
  }
}
