<template>
    <div class="container-fluid">
        <h1>Register</h1>
        <form @submit.prevent="createAccount()">
            <p v-if="message && message.detail" class="red-text red lighten-4 p-4">{{ message.detail }}</p>
            <div class="mb-2">
                <label for="inputUsername" class="form-label">Username</label>
                <input v-model="user.username" type="text" id="inputUsername" class="form-control" aria-describedby="usernameHelpBlock">
                <div id="usernameHelpBlock" class="form-text">
                Username help.
                </div>
            </div>
            <div class="mb-2">
                <label for="inputEmail" class="form-label">Email</label>
                <input v-model="user.email" type="email" id="inputEmail" class="form-control" aria-describedby="emailHelpBlock">
                <div id="emailHelpBlock" class="form-text">
                Email help.
                </div>
            </div>
            <div class="mb-2">
                <label for="inputPassword" class="form-label">Password</label>
                <input v-model="user.password" type="password" id="inputPassword" class="form-control" aria-describedby="passwordHelpBlock">
                <div id="passwordHelpBlock" class="form-text">
                Your password must be 8-20 characters long, contain letters and numbers, and must not contain spaces, special characters, or emoji.
                </div>
            </div>
            <button class="btn blue accent-2">Create Account</button>
        </form>
    </div>
</template>

<script>
export default {
    data(){
        return {
            user: {
                "username": "",
                "email": "",
                "password": ""
            },
            message: null
        }
    },
    methods:{
        async createAccount(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/register', 'POST', this.user, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.$router.push("/login")
            }
        }
    }
}
</script>