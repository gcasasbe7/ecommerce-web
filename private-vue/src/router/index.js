import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Shop from '@/views/Shop.vue'
import Categories from '@/views/Categories.vue'
import Product from '@/views/Product.vue'
import Search from '@/views/Search.vue'
import Cart from '@/views/Cart.vue'
import Checkout from '@/views/Checkout.vue'
import Identify from '@/views/Identify.vue'
import store from '../store'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/About.vue')
  },
  {
    path: '/search',
    name: 'Search',
    component: Search
  },
  {
    path: '/login',
    name: 'Identify',
    component: Identify
  },
  {
    path: '/cart',
    name: 'Cart',
    component: Cart
  },
  {
    path: '/cart/checkout',
    name: 'Checkout',
    component: Checkout
  },
  {
    path: '/shop',
    name: 'Categories',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: Categories
  },
  {
    path: '/shop/:category_slug',
    name: 'CategoryDetail',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: Shop
  },
  {
    path: '/shop/:category_slug/:product_slug',
    name: 'ProductDetail',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: Product
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  // Persist the previous path in the Vuex Store
  scrollBehavior(to, from, savedPosition) {
    store.state.previousPath = from.fullPath},
})

export default router
