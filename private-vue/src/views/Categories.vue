<template>
    <div class="product-page">
        <div class="row">
            <CategoryBox 
                v-for="category in this.categories" 
                v-bind:key="category"
                v-bind:category="category"
            />
        </div>
    </div>
</template>

<script>
import ApiHelper from '@/helpers/api_helper'
import CategoryBox from '@/components/CategoryBox.vue'

export default {
    name: 'Product',
    data() {
        return {
            categories: [],
        }
    },
    components: {
        CategoryBox
    },
    mounted() {
        document.title = "Categories | iPadel"
        this.getCategories()
    },
    methods: {
        async getCategories() {
            // Declare the callbacks
            const callback = {
                success: (response) => {
                    this.categories = response.data.categories

                    if(response.data.highlight){
                        this.categories.push(response.data.highlight)
                    }
                },
                error: (error) => {
                    // Todo: Error messaging
                    console.log(error)
                }
            }

            // Fetch the current category detail from the Api
            ApiHelper.getCategories(callback)
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
