<template>
    <div class="product-page">
        <div class="row">
            <div class="column">
                <router-link v-bind:to="`/shop/${category_slug}`">Continue shopping</router-link>
                <img v-bind:src="product.image_absolute_url" style="width:400px;height:400px;">
            </div>
            <div class="column">
                <h1>{{product.name}} (${{product.price}})</h1>
                <h1>{{product.display_image}}</h1>
                <h2>{{product.description}}</h2>
            </div>
        </div>
        
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Product',
    data() {
        return {
            product: {},
            category_slug: "",
        }
    },
    mounted() {
        this.getProduct()
    },
    methods: {
        async getProduct() {
            this.$store.commit('setIsApplicationLoading', true)

            this.category_slug = this.$route.params.category_slug
            const productSlug = this.$route.params.product_slug

            await axios
                .get(`/api/v1/shop/${this.category_slug}/${productSlug}`)
                .then(response => {
                    this.product = response.data

                    document.title = this.product.name + " | iPadel"
                })
                .catch(error => {
                    console.log(error)
                })

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
  height: 300px; /* Should be removed. Only for demonstration */
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}
</style>
