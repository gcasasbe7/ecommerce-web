<template>
    <div class="product-box">
        <img v-bind:src="product.image_absolute_url" style="width:400px;height:400px;">

        <h1>{{product.name}} (${{product.price}})</h1>
        <h1>{{product.cover_image}}</h1>
        <h2>{{product.description}}</h2>

        <router-link v-bind:to="product.absolute_url">View details</router-link>
        <button @click="addToCart">Add to cart</button>
    </div>
</template>

<script>
export default {
    name: 'ProductBox',
    props: {
        product: Object,
    },
    methods: {
        addToCart(){
            this.$store.commit('setIsApplicationLoading', true)

            const item = {
                'product': this.product,
                'quantity': 1
            }

            this.$store.commit('addToCart', item)

            this.$store.commit('setIsApplicationLoading', false)
        }
    }
    
}
</script>