<template>
    <div class="me">
        <h1>Hello {{$store.state.user.name}}</h1>
        <br>
        <button @click="logout">Log out</button>
    </div>
</template>

<script>
export default {
    name: 'Me',
    data () {
        return {
            
        }
    },
    methods: {
        logout() {
            this.$store.commit('onLogoutUser')
        }
    }
}
</script>