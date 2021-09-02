<template>
    <div class="cart-item">
        <div class="row">
            <div class="column">
                <img v-bind:src="this.item.product.image_absolute_url" style="width:160px;height:160px;">
            </div>
            <div class="column">
                <h2>{{this.item.product.name}} x {{this.item.quantity}}  {{totalPrice}}</h2>
                <button @click="decreaseQuantity(this.item)">-</button>
                <button @click="increaseQuantity(this.item)">+</button><br>

                <button @click="removeItem(this.item)"><i class="fa fa-trash"></i></button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CartItem',
    props: {
        cartItem: Object,
    },
    data() {
        return {
            item: this.cartItem,
        }
    },
    computed: {
        totalPrice() {
            return '(' + (this.item.product.price * this.item.quantity).toFixed(2) + '€)'
        }
    },
    methods: {
        increaseQuantity(item){
            item.quantity += 1

            this.updateCart()
        },
        decreaseQuantity(item){
            if(item.quantity > 1) {
                item.quantity -= 1
            }
            this.updateCart()
        },
        removeItem(item){
            this.$store.commit('removeFromCart', item)
        },
        updateCart() {
            localStorage.setItem('cart', JSON.stringify(this.$store.state.cart))

        }
    },
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