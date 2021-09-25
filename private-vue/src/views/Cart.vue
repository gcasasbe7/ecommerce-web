<template>
<div class="cart-page">
    <div v-if="this.cartSize > 0">
        <h1>Your cart ({{cartSize}} items)</h1>
        <h2>Total: {{cartTotalPrice}}€</h2>
        <button class="mb-5" @click="clearCart">Clear cart</button>

        <CartItem v-on:itemModified="updateTitle" v-for="item in this.cart.items" v-bind:key="item.product.id" v-bind:cartItem="item" v-bind:editable="true" />

        <router-link to="/cart/checkout"><button>Proceed to checkout</button></router-link>
    </div>
    <div v-else>
        <h1>Cart empty view</h1>
    </div>
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
    methods: {
        clearCart() {
            this.$store.commit('clearCart')
        },
        updateTitle() {
            document.title = `Cart (${this.cartSize}) | iPadel`
        },
    },
    computed: {
        cartSize() {
            return this.cart.items.reduce((acc, val) => {
                return acc += val.quantity
            }, 0)
        },
        cartTotalPrice() {
            const val = this.cart.items.reduce((acc, val) => {
                return acc += val.quantity * val.product.price
            }, 0)

            return val.toFixed(2)
        }
    },
}
</script>
