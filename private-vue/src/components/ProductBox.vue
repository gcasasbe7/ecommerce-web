<template>
    <div class="product-box">
        <img v-bind:src="product.image_absolute_url" style="width:400px;height:400px;">

        <h1>{{product.name}}</h1>
        <h1>{{product.display_image}}</h1>
        <h2>{{product.description}}</h2>

        <router-link v-bind:to="product.absolute_url">View details</router-link>
    </div>
</template>

<script>
export default {
    name: 'ProductBox',
    props: {
        product: Object
    }
    
}
</script>