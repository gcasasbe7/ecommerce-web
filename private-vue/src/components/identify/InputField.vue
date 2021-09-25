<template>
<div class="identify-field">
    <div class="mb-3">
        <label class="fl mb-1" v-bind:for="this.label">{{this.label}}</label>
        <input class="form-control" v-bind:type="this.type" v-bind:placeholder="this.placeholder" v-model="this.model">
    </div>
    <div class="identify-field-messages" v-if="this.errors.length > 0 && this.display_errors">
        <p v-for="error in errors" class="red" v-bind:key="error">{{error}}</p>
    </div>
</div>
</template>

<script>
export default {
    name: 'InputField',
    props: {
        type: String,
        validators: [Object],
        placeholder: String,
        display_errors: Boolean,
        password1: String,
        label: String,
        value: String,
    },
    mounted() {
        this.model = this.value
    },
    data() {
        return {
            model: '',
            errors: []
        }
    },
    methods: {
        validate() {
            // Clean previous errors
            this.errors = []
            // Declare result
            let result = true
            // Apply all the validations to the field
            this.validators.forEach(validator => {
                if (!validator.validate(this.model)) {
                    this.errors.push(validator.error)
                    result = false
                }
            });
            // Emit the result to the parent
            this.set_valid(result)
        },
        set_valid(is_valid) {
            this.$emit('set_valid', is_valid, this.model)
        }
    },
    watch: {
        'model': function () {
            this.validate()
        },
        'display_errors': function () {
            this.validate()
        },
        'password1': function () {
            this.validate()
        }
    }
}
</script>

<style scoped>
.fl {
    float: left;
}
</style>