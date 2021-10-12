<template>
<div class="cart-item mb-5">
    <div class="container">
        <div v-if="this.editable">
            <div class="row">
                <div class="col-sm-8">
                    <div class="row">
                        <div class="col-sm-4">
                            <img v-bind:src="this.item.product.image_absolute_url" style="width:120px;height:120px;">
                        </div>
                        <div class="col-sm-6">
                            <p class="cv">{{this.item.product.name}} {{totalPrice}}</p>
                        </div>
                    </div>

                </div>
                <div class="col-sm-2">
                    <button @click="decreaseQuantity(this.item)">-</button>
                    {{this.item.quantity}}
                    <button @click="increaseQuantity(this.item)">+</button>
                </div>
                <div class="col-sm-2">
                    <button @click="removeItem(this.item)"><i class="fa fa-trash"></i></button>
                </div>
            </div>
        </div>
        <div v-else>
            <div class="row">
                <div class="col">
                    <img v-bind:src="this.item.product.image_absolute_url" style="width:120px;height:120px;">
                </div>
                <div class="col">
                    <p>{{this.item.product.name}} x {{this.item.quantity}} {{totalPrice}}</p>
                </div>
            </div>
        </div>
    </div>

</div>
</template>

<script>
export default {
    name: 'CartItem',
    props: {
        cartItem: Object,
        editable: Boolean
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
        increaseQuantity(item) {
            item.quantity += 1

            this.updateCart()
        },
        decreaseQuantity(item) {
            if (item.quantity > 1) {
                item.quantity -= 1
            }
            this.updateCart()
        },
        removeItem(item) {
            this.$store.commit('removeFromCart', item)
            // Notify the Cart view
            this.$emit('itemModified')
        },
        updateCart() {
            localStorage.setItem('cart', JSON.stringify(this.$store.state.cart))
            // Notify the Cart view
            this.$emit('itemModified')
        }
    },
}
</script>

<style scoped>
* {
    box-sizing: border-box;
}

img {
    border-radius: 20%;
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

.cv {
    height: 100px;
    line-height: 100px;
    text-align: center;
}
</style>
