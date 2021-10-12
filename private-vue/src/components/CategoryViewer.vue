<template>
    <div class="category-page">
        <h1>{{this.category.name}}</h1>

        <ProductBox 
            v-for="product in this.category.products" 
            v-bind:key="product.id"
            v-bind:product="product"
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