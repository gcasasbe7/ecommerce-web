<template>
    <div class="cart-page">

    <h1>Your cart ({{cartSize}} items)</h1>
    <h2>Total: {{cartTotalPrice}}€</h2>
    <button @click="clearCart">Clear cart</button>

    <CartItem 
        v-on:itemModified="updateTitle"
        v-for="item in this.cart.items" 
        v-bind:key="item.product.id"
        v-bind:cartItem="item"
        />

    <router-link to="/cart/checkout"><button>Proceed to checkout</button></router-link>
    </div>
</template>

<script>
import CartItem from '@/components/cart/CartItem.vue'

export default {
    name: 'Cart',
    data() {
        return {
            cart: {
                items: [],
            }
        }
    },
    components: {
        CartItem,
    },
    mounted() {
        this.cart = this.$store.state.cart
        document.title = `Cart (${this.cartSize}) | iPadel`
    },
    computed: {
        cartSize() {
            return this.cart.items.reduce((acc, val) => {
                return acc += val.quantity
            }, 0)
        },
        cartTotalPrice() {
            const val =  this.cart.items.reduce((acc, val) => {
                return acc += val.quantity * val.product.price
            }, 0)

            return val.toFixed(2)
        }
    },
    methods: {
        clearCart() {
            this.$store.commit('clearCart')
        },
        updateTitle() {
            document.title = `Cart (${this.cartSize}) | iPadel`
        }
    },
}
</script>