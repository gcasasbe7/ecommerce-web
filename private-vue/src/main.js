import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import LogIn from '@/components/identify/LogIn.vue'
import SignUp from '@/components/identify/SignUp.vue'

// Bootstrap import
import 'bootstrap/dist/css/bootstrap.min.css'
import 'jquery/src/jquery.js'
import 'bootstrap/dist/js/bootstrap.min.js'

// Define axios Base URL
axios.defaults.baseURL = 'http://127.0.0.1:8000'

// Create the main Vue app
const app = createApp(App)
// Bind the route and the Vuex store and mount the app in the root divider
app.use(store).use(router).mount('#app')
// Custom components declaration for global use
app.component('LogIn', LogIn)
app.component('SignUp', SignUp)