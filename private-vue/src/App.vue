<template>
<div id="nav">
    <div class="red" v-if="$store.state.isApplicationLoading">
        APPLICATION LOADING
    </div>

    <div v-if="$store.getters.is_user_logged_in">
        <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link> |
        <router-link to="/shop">Shop</router-link> |
        <router-link to="/cart">Cart ({{cartSize}})</router-link> |
        <router-link to="/me">{{$store.state.user.name}}</router-link>
    </div>
    <div v-else>
        <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link> |
        <router-link to="/shop">Shop</router-link> |
        <router-link to="/cart">Cart ({{cartSize}})</router-link> |
        <router-link to="/identify">Account</router-link>
    </div>

    <div>
        <form method="get" action="/search">
            <input type="text" class="input" name="query" placeholder="Search anything..." v-model="this.search_query">
            <div class="control">
                <button @click="submit_search">
                    <span class="icon">
                        <i class="fas fa-search"></i>
                    </span>
                </button>
            </div>
        </form>
    </div>
</div>
<router-view />
</template>

<script>
export default {
    data() {
        return {
            cart: {
                items: [],
            },
            search_query: ''
        }
    },
    beforeCreate() {
        this.$store.commit('initializeStore')
    },
    mounted() {
        this.cart = this.$store.state.cart
    },
    computed: {
        cartSize() {
            return this.cart.items.reduce((acc, val) => {
                return acc += val.quantity
            }, 0)
        }
    },
    methods: {
        // Prevent the search for empty queries
        submit_search(e) {
            if (this.search_query.length < 1) {
                e.preventDefault();
            }
        }
    }
}
</script>

<style lang="scss">
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
}

#nav {
    padding: 30px;

    a {
        font-weight: bold;
        color: #2c3e50;

        &.router-link-exact-active {
            color: #42b983;
        }
    }
}

.red {
    color: #850101;
}

.fl {
    float: left;
}
</style>
