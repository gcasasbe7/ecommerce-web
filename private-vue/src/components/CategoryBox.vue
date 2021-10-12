<template>
    <div class="category-box">
        <img v-bind:src="category.image_url" style="width:700px;height:700px;">
        <h1>{{category.name}}</h1>

        <router-link v-bind:to="category.absolute_url">View details</router-link>
    </div>
</template>

<script>
export default {
    name: 'CategoryBox',
    props: {
        category: Object,
    }
    
}
</script>