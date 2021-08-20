<template>
    <div class="category-page">
        <div class="row">
            <div class="column">
                <h2>Product Categories</h2>
                
                <div v-for="category in all_categories" :key="category.id">
                    <router-link v-bind:to="category.absolute_url">{{category.name}}</router-link>
                </div>
            </div>
            <div class="column">
                <CategoryViewer :category="this.selected_category"/>
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
            selected_category: {},
            all_categories: [],
            default_category_slug: ""
        }
    },
    components: {
        CategoryViewer,
    },
    mounted() {
        document.title = "Shop | iPadel"
        this.getData()
    },
    watch: {
        $route(to, from) {
            if(to.name === 'CategoryDetail'){
                this.getCategoryFromUrl()
            } else if(to.name == 'Shop') {
                this.getCategory(this.default_category_slug)
            }
        }
    },
    methods: {
        async getData() {
            // Assert the application is loading
            this.$store.commit('setIsApplicationLoading', true)

            // Build the request
            const url = "/api/v1/shop"
            await axios
                .get(url)
                .then(response => {
                    this.all_categories = response.data.categories
                    this.default_category_slug = response.data.default
                })
                .catch(error => {
                    console.log(error)
                })
            
            // Is there a specified category in the URL?
            const categorySlug  = this.$route.params.category_slug

            if(categorySlug === undefined) {
                this.getCategory(this.default_category_slug)
            }else {
                this.getCategoryFromUrl()
            }

            // const categoryParam = (categorySlug === undefined) ? "" : `/shop/${categorySlug}/`

            // if(categoryParam && categoryParam.length > 0){
            //     this.all_categories.every((category, index) => {
            //         if(category.absolute_url === categoryParam){
            //             this.selected_category = category
            //             document.title = this.selected_category.name + " | iPadel"
            //             // Category found, break the loop
            //             return false
            //         }
            //         // Category not found, continue looping
            //         return true
            //     })
            // }

            // Assert we have finished loading the view
            this.$store.commit('setIsApplicationLoading', false)
        },
        async getCategoryFromUrl() {
            this.$store.commit('setIsApplicationLoading', true)

            const categorySlug = this.$route.params.category_slug

            await axios
                .get(`/api/v1/shop/${categorySlug}/`)
                .then(response => {
                    this.selected_category = response.data

                    document.title = this.selected_category.name + " | iPadel"
                })
                .catch(error => {
                    console.log(error)
                })

            this.$store.commit('setIsApplicationLoading', false)
        },

        async getCategory(category_slug) {
            this.$store.commit('setIsApplicationLoading', true)

            await axios
                .get(`/api/v1/shop/${category_slug}/`)
                .then(response => {
                    this.selected_category = response.data

                    document.title = this.selected_category.name + " | iPadel"
                })
                .catch(error => {
                    console.log(error)
                })

            this.$store.commit('setIsApplicationLoading', false)
        },
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
