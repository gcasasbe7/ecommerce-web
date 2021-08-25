<template>
    <div class="identify-field">
        <br><input 
            v-bind:type="this.type" 
            v-bind:placeholder="this.placeholder"
            v-model="this.model">

        <div class="signup-messages" v-if="errors.length > 0">
            <p v-for="error in errors" class="red" v-bind:key="error">{{error}}</p>
        </div>
    </div>    
</template>

<script>
export default {
    name: 'IdentifyField',
    props: {
        type: String,
        validators: [Object],
        placeholder: String
    },
    data() {
        return {
            model: '',
            is_valid: false,
            errors: []
        }
    },
    methods: {
        validate(){
            this.errors = []

            if(this.model.length > 0){
                this.validators.forEach(validator => {
                    if(!validator.regex.test(this.model)){
                        this.errors.push(validator.error)
                        this.is_valid = false
                    }
                });
            }
            
            return this.is_valid
        }
    },
    watch: {
        'model' : function() {
            this.validate()
        }
    }
}
</script>
