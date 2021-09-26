<template>
<div class="checkout-page">
    <div class="container">
        <div class="row">
            <div class="col-md-6 justify-content-md-center" style="padding: 50px 130px 50px 130px">
                <div class="mb-5">
                    Your basket: <h2>{{this.cartTotalPrice}}€</h2>
                </div>
                <CartItem v-for="item in this.cart.items" v-bind:key="item.product.id" v-bind:cartItem="item" v-bind:editable="false" />
            </div>
            <div class="col-md-6 justify-content-md-center" style="background-color: #F2F2F2; padding: 50px 100px 50px 100px">
                <form id="payment-form" @submit.prevent="submit_payment_form">

                    <!-- User Form Area -->
                    <div class="user-area mb-5">
                        <h3 class="mb-4">Contact Information</h3>
                        <div class="row">
                            <div class="col-sm-6">
                                <InputField @set_valid="set_valid_name" :label="this.name_field.label" :type="this.name_field.type" :validators="this.name_field.validators" :placeholder="this.name_field.placeholder" :display_errors="this.display_errors" />
                            </div>
                            <div class="col-sm-6">
                                <InputField @set_valid="set_valid_surname" :label="this.surname_field.label" :type="this.surname_field.type" :validators="this.surname_field.validators" :placeholder="this.surname_field.placeholder" :display_errors="this.display_errors" />
                            </div>
                        </div>
                        <div class="email-input mb-3">
                            <InputField @set_valid="set_valid_email" :label="this.email_field.label" :type="this.email_field.type" :validators="this.email_field.validators" :placeholder="this.email_field.placeholder" :display_errors="this.display_errors" />
                        </div>

                        <div class="phone-input">
                            <InputField @set_valid="set_valid_phone" :label="this.phone_field.label" :type="this.phone_field.type" :validators="this.phone_field.validators" :placeholder="this.phone_field.placeholder" :display_errors="this.display_errors" />
                            <small class="fl">We'll contact you during the shipping process if required</small>
                        </div>
                    </div>

                    <!-- Billing and Shipping address -->
                    <h3 class="mb-4" style="margin-top:60px">Shipping Information</h3>
                    <div class="shipping-area mb-3">
                        <div class="address-input mb-3">
                            <InputField @set_valid="set_valid_address" :label="this.address_field.label" :type="this.address_field.type" :validators="this.address_field.validators" :placeholder="this.address_field.placeholder" :display_errors="this.display_errors" />
                        </div>

                        <div class="place">
                            <div class="row">
                                <div class="col-sm-8">
                                    <InputField @set_valid="set_valid_city" :label="this.city_field.label" :type="this.city_field.type" :validators="this.city_field.validators" :placeholder="this.city_field.placeholder" :display_errors="this.display_errors" />
                                </div>
                                <div class="col-sm-4">
                                    <InputField @set_valid="set_valid_zipcode" :label="this.zipcode_field.label" :type="this.zipcode_field.type" :validators="this.zipcode_field.validators" :placeholder="this.zipcode_field.placeholder" :display_errors="this.display_errors" />
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Payment Form Area -->
                    <h3 class="mb-4">Payment Information</h3>
                    <div class="payment-area">
                        <label for="card-element" class="fl">Debit/Credit Card</label><br>
                        <div id="card-element"></div>
                        <button id="submit">
                            <div class="spinner hidden" id="spinner"></div>
                            <span id="button-text">Pay now <i class="fa fa-lock" aria-hidden="true"></i></span>
                        </button>
                        <p id="card-error" role="alert"></p>
                        <p class="result-message hidden">
                            Payment succeeded, see the result in your
                            <a href="" target="_blank">Stripe dashboard.</a> Refresh the page to pay again.
                        </p>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import ApiHelper from '@/helpers/api_helper.js'
import CartItem from '@/components/cart/CartItem.vue'
import config from '@/components/identify/config/checkout_config.js'
import InputField from '@/components/identify/InputField.vue'

export default {
    name: 'Checkout',
    components: {
        InputField
    },
    data() {
        return {
            cart: {
                items: []
            },
            valid_card_field: false,
            name_field: config.name_field,
            surname_field: config.surname_field,
            email_field: config.email_field,
            phone_field: config.phone_field,
            address_field: config.address_field,
            city_field: config.city_field,
            zipcode_field: config.zipcode_field,
            display_errors: false,
            errors: [],
            client_secret: '',
            card: {}
        }
    },
    components: {
        CartItem,
    },
    mounted() {
        // Fetch the data from the Vuex store
        this.cart = this.$store.state.cart
        this.email_field.value = this.$store.state.user.email
        this.name_field.value = this.$store.state.user.name
        this.surname_field.value = this.$store.state.user.surname
        this.email_field.value = "test"
        // Set the title
        document.title = "Checkout | iPadel"
        // Build the card element
        this.init_card()
    },
    methods: {
        submit_payment_form() {
            this.display_errors = false
            if (this.is_valid_form()) {
                this.checkout()
            } else {
                this.display_errors = true
            }
        },
        is_valid_form() {
            return this.name_field.is_valid &&
                this.surname_field.is_valid &&
                this.email_field.is_valid &&
                this.phone_field.is_valid &&
                this.address_field.is_valid &&
                this.city_field.is_valid &&
                this.zipcode_field.is_valid &&
                this.valid_card_field
        },
        checkout() {
            if (this.client_secret) {
                this.confirm_payment()
            } else {
                // Build the request data
                let data = {
                    "basket": {
                        "basket_creation_date": this.$store.state.cart.creation_date,
                        "basket_content": this.$store.getters.get_formatted_cart
                    }
                }

                // Declare the callbacks
                const callback = {
                    /* Successful checkout */
                    success: (response) => {
                        this.client_secret = response.data.client_secret
                        this.confirm_payment()
                    },
                    /* Unsuccessful checkout */
                    error: (error) => {
                        console.log(error)
                    },
                    /* Unrecognised user */
                    unauth: () => {
                        // Attempt to refresh the user access token
                        ApiHelper.refreshToken({
                            do: () => { 
                                console.log("Re attempting checkout after acces token expiry")
                                this.checkout() 
                            }
                        })
                    }
                }

                // Fetch the current category detail from the Api
                ApiHelper.checkout(callback, data)
            }
        },
        confirm_payment() {
            var ref = this
            stripe
                .confirmCardPayment(this.client_secret, {
                    payment_method: {
                        card: this.card
                    }
                })
                .then(function (result) {
                    if (result.error) {
                        // Show error to your customer
                        ref.show_error(result.error.message);
                    } else {
                        // The payment succeeded!
                        console.log("PAYMENT COMPLETE")
                    }
                });
        },
        show_error(errorMsgText) {
            var errorMsg = document.querySelector("#card-error");
            errorMsg.textContent = errorMsgText;
            setTimeout(function () {
                errorMsg.textContent = "";
            }, 5000);
        },
        init_card() {
            // Initialize Stripe elements
            var elements = stripe.elements();
            // Declare the card element styling
            var style = {
                base: {
                    // color: "#32325d",
                    fontFamily: 'Avenir, Helvetica, Arial, sans-serif',
                    fontSmoothing: "antialiased",
                    fontSize: "16px",
                    // "::placeholder": {
                    //     color: "#32325d"
                    // }
                },
                invalid: {
                    fontFamily: 'Avenir, Helvetica, Arial, sans-serif',
                    color: "#fa755a",
                    iconColor: "#fa755a"
                }
            };
            // Bind the style to the card stripe element
            this.card = elements.create("card", {
                hidePostalCode: true,
                style: style
            });
            // Stripe injects an iframe into the DOM
            this.card.mount("#card-element");
            document.querySelector("#submit").disabled = true
            var reference = this
            var set_card_complete = function (ref, value) {
                ref.valid_card_field = value
            }
            this.card.on("change", function (event) {
                // Disable the Pay button if there are no card details in the Element
                set_card_complete(reference, event.complete)
                document.querySelector("#submit").disabled = !event.complete
                document.querySelector("#card-error").textContent = event.error ? event.error.message : ""
            });
        },
        set_valid_name(is_valid, value) {
            this.name_field.is_valid = is_valid
            this.name_field.value = value
        },
        set_valid_surname(is_valid, value) {
            this.surname_field.is_valid = is_valid
            this.surname_field.value = value
        },
        set_valid_email(is_valid, value) {
            this.email_field.is_valid = is_valid
            this.email_field.value = value
        },
        set_valid_phone(is_valid, value) {
            this.phone_field.is_valid = is_valid
            this.phone_field.value = value
        },
        set_valid_address(is_valid, value) {
            this.address_field.is_valid = is_valid
            this.address_field.value = value
        },
        set_valid_city(is_valid, value) {
            this.city_field.is_valid = is_valid
            this.city_field.value = value
        },
        set_valid_zipcode(is_valid, value) {
            this.zipcode_field.is_valid = is_valid
            this.zipcode_field.value = value
        },
        getItemTotal(item) {return (item.quantity * item.product.price).toFixed(2)},
    },
    computed: {
        cartSize() {
            return this.cart.items.reduce((acc, val) => {
                return acc += val.quantity
            }, 0)
        },
        cartTotalPrice() {
            const val = this.cart.items.reduce((acc, val) => {
                return acc += val.quantity * val.product.price
            }, 0)
            return val.toFixed(2)
        }
    }
}
</script>

<style scoped>
.result-message {
    line-height: 22px;
    font-size: 16px;
}

.result-message a {
    color: rgb(89, 111, 214);
    font-weight: 600;
    text-decoration: none;
}

.hidden {
    display: none;
}

#card-error {
    color: rgb(105, 115, 134);
    text-align: left;
    font-size: 13px;
    line-height: 17px;
    margin-top: 12px;
}

#card-element {
    border-radius: 4px 4px 0 0;
    padding: 12px;
    border: 1px solid rgba(50, 50, 93, 0.1);
    height: 44px;
    width: 100%;
    background: white;
}

#payment-request-button {
    margin-bottom: 32px;
}

/* Buttons and links */
button {
    background: #5469d4;
    color: #ffffff;
    font-family: Arial, sans-serif;
    border-radius: 0 0 4px 4px;
    border: 0;
    padding: 12px 16px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    display: block;
    transition: all 0.2s ease;
    box-shadow: 0px 4px 5.5px 0px rgba(0, 0, 0, 0.07);
    width: 100%;
}

button:hover {
    filter: contrast(115%);
}

button:disabled {
    opacity: 0.5;
    cursor: default;
}
</style>
