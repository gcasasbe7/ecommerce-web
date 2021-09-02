<template>
    <div class="product-dialog">
        <!-- todo: import dialog from styles lib -->
        <img v-bind:src="product.cover_image">

        <h1>{{product.name}}</h1>
        <h2>{{product.description}}</h2>

        <router-link v-bind:to="product.absolute_url">View details</router-link>
    </div>
</template>

<script>
export default {
    name: 'Product Dialog',
    props: {
        product: Object
    }
    
}
</script>