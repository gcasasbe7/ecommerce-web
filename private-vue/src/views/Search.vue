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
import ApiHelper from '@/helpers/api_helper.js'
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
            // Declare the callbacks
            const callback = {
                success: (response) => {
                    this.products = response.data.result
                },
                error: (error) => {
                    console.log(error)
                }
            }

            // Perform the search in the backend application
            ApiHelper.performSearch(callback, {'query':this.query})
        }
    }
}
</script>