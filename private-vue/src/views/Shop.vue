<template>
<div class="category-page">
    <div class="container">
        <div class="row">
            <div class="column">
                <h2>Product Categories</h2>

                <div v-for="category in all_categories" :key="category">
                    <router-link v-bind:to="category.absolute_url">{{category.name}}</router-link>
                </div>
            </div>
            <div class="column">
                <CategoryViewer :category="this.selected_category" />
            </div>
        </div>
    </div>
</div>
</template> 

<script>
import ApiHelper from '@/helpers/api_helper'
import CategoryViewer from '@/components/CategoryViewer'
import CategoryBox from '@/components/CategoryBox'

export default {
    name: 'CategoryView',
    data() {
        return {
            selected_category: {},
            all_categories: [],
        }
    },
    components: {
        CategoryViewer,
        CategoryBox,
    },
    mounted() {
        document.title = "Shop | iPadel"
        this.getCategoryFromUrl()
    },
    watch: {
        $route(to, from) {
            if (to.name === 'CategoryDetail') {
                this.getCategoryFromUrl()
            }
        }
    },
    methods: {
        async getCategoryFromUrl() {
            // Fetch the url param
            const categorySlug = this.$route.params.category_slug

            // Declare the callbacks
            const callback = {
                success: (response) => {
                    // Do we have products to display in the current category?
                    if (response.data.category_detail.products.length > 0) {
                        this.selected_category = response.data.category_detail
                        this.all_categories = response.data.all_categories
                        document.title = this.selected_category.name + " | iPadel"
                    } else {
                        // Redirect to the main shop view
                        this.$router.push('/shop')
                    }
                },
                error: (error) => {
                    this.$router.push('/shop')
                }
            }

            // Fetch the current category detail from the Api
            ApiHelper.getCategoryDetail(callback, categorySlug)
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
