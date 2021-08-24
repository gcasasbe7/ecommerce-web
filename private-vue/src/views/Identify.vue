<template>
    <div class="identify-page">
        <h1>WELCOME USER!</h1>
        <div class="row">
            <div class="column">
                <h2>ALREADY REGISTERED? LOG IN!</h2>
                <div class="login-messages" v-if="login_messages.length > 0">
                    <p v-for="message in login_messages" class="red" v-bind:key="message">{{message}}</p>
                </div>
                <form @submit.prevent="submitForm(0)">
                    <br><input type="text" name="userEmail" placeholder="Email" v-model="l_email">
                    <br><input type="password" name="userPassword" placeholder="Password" v-model="l_password">
                    <br><br><button type="submit">Log in</button>
                </form>
            </div>
            <div class="column">
                <h2>FIRST TIME HERE? REGISTER!</h2>
                <div class="signup-messages" v-if="signup_messages.length > 0">
                    <p v-for="message in signup_messages" class="red" v-bind:key="message">{{message}}</p>
                </div>
                <form @submit.prevent="submitForm(1)">
                    <br><input type="text" name="userName" placeholder="Name" v-model="s_name">
                    <br><input type="text" name="userSurname" placeholder="Surname" v-model="s_surname">
                    <br><input type="text" name="userEmail" placeholder="Email" v-model="s_email">
                    <br><input type="password" name="userPassword" placeholder="Password" v-model="s_password">
                    <br><input type="password" name="userPassword2" placeholder="Repeat password" v-model="s_password2">
                    <br><br><button type="submit">Register</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Identify',
    data() {
        return {
            // Login fields
            l_email: '',
            l_password: '',
            // Registration fields
            s_email: '',
            s_name: '',
            s_surname: '',
            s_password: '',
            s_password2: '',
            login_messages: [],
            signup_messages: [],
        }
    },
    methods: {
        submitForm(form_id) {
            if(form_id === 0){
                // Log in form submitted
                this.login_messages = []
                if(this.login_sanity_check()){
                    
                }

            }else {
                // Registration form submitted
                this.signup_messages = []
                if(this.signup_sanity_check()){
                    const data = {
                        'email' : this.s_email,
                        'name' : this.s_name,
                        'surname' : this.s_surname,
                        'password' : this.s_password,
                    }
                    this.completeSignup(data)
                }
            }
        },

        login_sanity_check() {
            return this.validateEmail(this.l_email, 0)
        },

        signup_sanity_check(){
            const valid_email = this.validateEmail(this.s_email, 1)
            const valid_name = this.validateText(this.s_name, "name", 1)
            const valid_surname = this.validateText(this.s_surname,"surname", 1)
            const valid_password = this.validatePasswords(this.s_password,this.s_password2, 1)

            return valid_email && valid_name && valid_surname && valid_password
        },

        validateEmail(email, form_id) {
            const valid_email = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email)

            if(!valid_email){
                const error = "Please introduce a valid email"
                form_id == 0 ? this.login_messages.push(error) : this.signup_messages.push(error)
                return false
            }
            return true
        },

        validatePasswords(password, password2, form_id){
            // Both passwords match
            const valid_match = password === password2

            // Minimum length 8
            const valid_len = /[a-zA-Z0-9]{8,}$/.test(password)

            // Contains a number
            const valid_num = /\d/.test(password)

            // Contains mayusc
            const valid_mayusc = /[A-Z]/.test(password)


            // Buffer the possible errors
            if(!valid_match){
                const error = "Please ensure both passwords match"
                form_id == 0 ? this.login_messages.push(error) : this.signup_messages.push(error)
            }

            if(!valid_len){
                const error = "For security reasons, please ensure your password is at least 8 characters long"
                form_id == 0 ? this.login_messages.push(error) : this.signup_messages.push(error)
            }

            if(!valid_num){
                const error = "For security reasons, please ensure your password contains at least one number"
                form_id == 0 ? this.login_messages.push(error) : this.signup_messages.push(error)
            }

            if(!valid_mayusc){
                const error = "For security reasons, please ensure your password contains at least one capital letter"
                form_id == 0 ? this.login_messages.push(error) : this.signup_messages.push(error)
            }

            // Return the validity of the password
            return valid_match && valid_len && valid_num && valid_mayusc
        },

        validateText(text, param, form_id){
            const valid_text = text !== undefined && text.length > 0

            if(!valid_text){
                const error = `Please introduce a valid ${param}`
                form_id == 0 ? this.login_messages.push(error) : this.signup_messages.push(error)
                return false
            }
            return true
        },
        completeSignup(form_data){
            console.log("hello")
            axios  
                .post("/api/v1/users/", form_data)
                .then(response => {
                    console.log(`An email has been sent to ${this.s_email}. Please verify your account by pressing the link provided inside the email content.`)
                    // Display dialog with the above message
                })
                .catch(error => {
                    if(error.response){
                        for(const property in error.response.data){
                            //console.log("wtf")
                            //this.signup_messages.push(`${property}: ${error.response.data[property]} `)
                        }
                    } else if (error.message) {
                        this.signup_messages.push("Something went wrong")
                    }
                })
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

.red {
    color: red
}
</style>