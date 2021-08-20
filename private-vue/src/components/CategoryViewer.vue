<template>
    <div class="category-page">
        <h1>{{this.category.name}}</h1>

        <ProductBox 
            v-for="product in this.category.products" 
            v-bind:key="product.id"
            v-bind:product="product"
            v-bind:product_detail_url="`${this.category.absolute_url}${product.absolute_url}`"
            />
    </div>
</template>

<script>
import axios from 'axios'
import ProductBox from '@/components/ProductBox'

export default {
    name: 'CategoryViewer',
    props: {
        category: Object,
    },
    data() {
        return {
            
        }
    },
    components: {
        ProductBox,
    }
}
</script>