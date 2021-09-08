<template>
<div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <!-- <HelloWorld msg="iPadel"/> -->
    <br>
    <button @click="showSuccessToast">Show success toast</button>
    <button @click="showWarningToast">Show warning toast</button>
    <button @click="showErrorToast">Show error toast</button>

    <div class="toast-container position-absolute top-0 end-0 p-3">
        <div id="success_toast" class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="4500">
            <div class="toast-header">
                <div class="success rounded me-2" style="height:20px; width: 20px"></div>
                <strong class="me-auto">Item added to your basket</strong>
                <button type="button" class="btn-close" data-bs-dismiss="success_toast" aria-label="Close"></button>
            </div>
            <div class="toast-body toast-body-bg" style="background-color:">
                Siux Spartan has been added to your basket
            </div>
            <div class="toast-footer d-flex justify-content-center toast-footer-bg" style="padding:10px">
                <div class="vertical-center">
                    See my basket<i class="fa fa-chevron-right" aria-hidden="true" style="margin-left:10px"></i>
                </div>
            </div>
        </div>

        <div id="warning_toast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <div class="warning rounded me-2" style="height:20px; width: 20px"></div>
                <strong class="me-auto">Item added to your basket</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body toast-body-bg">
                Siux Spartan has been added to your basket
            </div>
            <div class="toast-footer d-flex justify-content-center toast-footer-bg" style="padding:10px">
                <div class="vertical-center">
                    See my basket<i class="fa fa-chevron-right" aria-hidden="true" style="margin-left:10px"></i>
                </div>
            </div>
        </div>

        <div id="error_toast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <div class="error rounded me-2" style="height:20px; width: 20px"></div>
                <strong class="me-auto">Item added to your basket</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body toast-body-bg">
                Siux Spartan has been added to your basket
            </div>
            <div class="toast-footer d-flex justify-content-center toast-footer-bg" style="padding:10px">
                <div class="vertical-center">
                    See my basket<i class="fa fa-chevron-right" aria-hidden="true" style="margin-left:10px"></i>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
    name: 'Home',
    components: {
        HelloWorld
    },
    mounted() {
        document.getElementsByClassName('toast').forEach(toast => {
            toast.addEventListener('hidden.bs.toast', function (toast) {
                $(`#${toast.target.id}`).hide()
            })
        });
    },
    methods: {
        showSuccessToast() {
            $('#success_toast').removeClass("fade")
            $('#success_toast').toast({
                'autohide': true
            })
            $('#success_toast').show({})
            $('#success_toast').toast('show')
        },
        showWarningToast() {
            $('#warning_toast').removeClass("fade")
            $('#warning_toast').toast({
                'autohide': true
            })
            $('#warning_toast').show({})
            $('#warning_toast').toast('show')
        },
        showErrorToast() {
            $('#error_toast').removeClass("fade")
            $('#error_toast').toast({
                'autohide': true
            })
            $('#error_toast').show({})
            $('#error_toast').toast('show')
        },
    }
}
</script>

<style scoped>
.toast-body-bg {
    background-color: #d3cfcf4f !important;
}

.toast-footer-bg {
    background-color: #ffffff !important;
}

.error {
    background-color: #ff0000 !important;
}

.warning {
    background-color: #ffe65b !important;
}

.success {
    background-color: #52cc42 !important;
}

.col-centered {
    float: none;
    margin: 0 auto;
}

.vertical-center {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
