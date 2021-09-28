<template>
<div class="product-page">
    <div class="container">
        <div class="row">
            <div class="column">
                <router-link v-bind:to="this.$store.state.previousPath">Continue shopping</router-link>
                <br>
                <img v-bind:src="product.image_absolute_url" style="width:400px;height:400px;">
                <img v-for="image in product.images" v-bind:key="image" v-bind:src="image.absolute_url" style="width:400px;height:400px;">

            </div>
            <div class="column">
                <h1>{{product.name}} ({{product.price}}€)</h1>
                <h1>{{product.cover_image}}</h1>
                <h2>{{product.description}}</h2>
                <br>
                <button @click="addToCart">Add to cart</button>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import ApiHelper from '@/helpers/api_helper.js'

export default {
    name: 'Product',
    data() {
        return {
            product: {},
        }
    },
    mounted() {
        this.getProduct()
    },
    methods: {
        async getProduct() {
            // Fetch the url param
            const categorySlug = this.$route.params.category_slug
            const productSlug = this.$route.params.product_slug

            // Declare the callbacks
            const callback = {
                success: (response) => {
                    this.product = response.data.product
                    document.title = this.product.name + " | iPadel"
                },
                error: (error) => {
                    // Todo: Error messaging
                    console.log(error)
                }
            }

            // Fetch the current category detail from the Api
            ApiHelper.getProductDetail(callback, categorySlug, productSlug)
        },
        addToCart() {
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

<style scoped>
* {
    box-sizing: border-box;
}

/* Create two equal columns that floats next to each other */
.column {
    float: left;
    width: 50%;
    padding: 10px;
    height: 300px;
    /* Should be removed. Only for demonstration */
}

/* Clear floats after the columns */
.row:after {
    content: "";
    display: table;
    clear: both;
}
</style>
