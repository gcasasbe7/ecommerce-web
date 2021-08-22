<template>
    <div class="product-page">
        <div class="row">
            <CategoryBox 
                v-for="category in this.categories" 
                v-bind:key="category.id"
                v-bind:category="category"
            />
        </div>
        
    </div>
</template>

<script>
import axios from 'axios'
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
            this.$store.commit('setIsApplicationLoading', true)

            await axios
                .get('/api/v1/categories')
                .then(response => {
                    this.categories = response.data
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
