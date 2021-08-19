<template>
    <div class="category-page">
        <div class="row">
            <div class="column">
                <h2>Column 2</h2>
                <p>Some text..</p>
            </div>
            <div class="column">
                <CategoryViewer :category="this.category"/>
            </div>
        </div>
        
    </div>
</template>

<script>
import axios from 'axios'
import CategoryViewer from '@/components/CategoryViewer'

export default {
    name: 'CategoryView',
    data() {
        return {
            category: {
                name: "",
                products : []
            }
        }
    },
    components: {
        CategoryViewer,
    },
    mounted() {
        // this.getData()
        this.getCategories()
    },
    methods: {
        /* 
        async getData() {
            // Assert the application is loading
            this.$store.commit('setIsApplicationLoading', true)

            // Is there a specified category in the URL?
            const categorySlug  = this.$route.params.category_slug
            const productSlug   = this.$route.params.product_slug

            // Build the request
            const categoryParam = (categorySlug === undefined) ? "" : categorySlug
            const productParam = (productSlug === undefined) ? "" : `/${productSlug}`
            const url = `/api/v1/shop/${categoryParam}${productParam}`
            await axios
                .get(url)
                .then(response => {
                    this.category = response.data

                    document.title = this.category.name
                })
                .catch(error => {
                    console.log(error)
                })
            
            // Assert we have finished loading the view
            this.$store.commit('setIsApplicationLoading', false)
        }
        */
        async getCategories() {
            this.$store.commit('setIsApplicationLoading', true)

            const categorySlug = this.$route.params.category_slug

            await axios
                .get(`/api/v1/shop/${categorySlug}/`)
                .then(response => {
                    this.category = response.data

                    document.title = this.category.name
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
