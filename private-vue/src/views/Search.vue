<template>
    <div class="search-page">
        <h1>{{ this.products.length }} results for "{{ this.query }}":</h1>

        <ProductBox 
            v-for="product in this.products" 
            v-bind:key="product.id"
            v-bind:product="product"
            />
    </div>
</template>

<script>
import axios from 'axios'
import ProductBox from '@/components/ProductBox.vue'

export default {
    name: 'Search',

    data() {
        return {
            products: [],
            query: ''
        }
    },
    components: {
        ProductBox
    },
    mounted() {
        this.getQuery()
    },
    methods: {
        getQuery() {
            let uri = window.location.search.substring(1)
            let params = new URLSearchParams(uri)

            if(params.get('query')){
                this.query = params.get('query')
                this.performSearch()
            }
        },

        async performSearch() {
            // Assert the application is loading
            this.$store.commit('setIsApplicationLoading', true)

            // Build the request
            const url = "/api/v1/products/search/"
            await axios
                .post(url, {'query' : this.query})
                .then(response => {
                    this.products = response.data
                })
                .catch(error => {
                    console.log(error)
                })

            // Assert we have finished loading the view
            this.$store.commit('setIsApplicationLoading', false)
        }
    }
}
</script>