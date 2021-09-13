<template>
<div class="checkout-page">
    <h1>Checkout page</h1>
</div>
</template>

<script>
export default {
    name: 'Checkout',
    data() {
        return {
            cart: {
                items: []
            },
            stripe: {},
            card: '',
            first_name: '',
            last_name: '',
            email: '',
            phone: '',
            address: '',
            zipcode: '',
            place: '',
            errors: []
        }
    },
    mounted() {
        this.cart = this.$store.state.cart
        document.title = "Checkout | iPadel"
    },
    methods: {
        getItemTotal(item) {
            return (item.quantity * item.product.price).toFixed(2)
        }
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
    }
}
</script>
