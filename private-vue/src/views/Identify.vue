<template>
    <div class="identify-page">
        <h1>WELCOME USER!</h1>
        <div class="row">
            <div class="column">
                <LogIn @submit_form="complete_login"/>
            </div>
            <div class="column">
                <SignUp @submit_form="complete_signup"/>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import SignIn from '@/components/identify/LogIn.vue'
import SignUp from '@/components/identify/SignUp.vue'

export default {
    name: 'Identify',
    components: [
        SignIn, SignUp
    ],
    methods: {
        complete_login(login_data){
            console.log("login", login_data)
        },

        complete_signup(signup_data){
            console.log("signup", signup_data)
            /*axios  
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
                })*/
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