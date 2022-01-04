<template>
    <div>
        <h1>Login</h1>
        <p>{{ message }}</p>
        <form @submit.prevent="getToken">
            <div class="mb-3">
                <label for="loginInput" class="form-label">Login to exisitng account</label>
                <input type="text" class="form-control" id="loginInput" v-model="login">
            </div>
            <div class="mb-3">
                <label for="passwordInput" class="form-label">Password</label>
                <input type="password" class="form-control" id="passwordInput" v-model="password" aria-describedby="passwordHelpBlock">
                <div id="passwordHelpBlock" class="form-text">Your password must be 8-20 characters long, contain letters and numbers, and must not contain spaces, special characters, or emoji.
                </div>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
        <router-link to="/register" class="link p-2">Create account</router-link>
    </div>
</template>

<script>
export default {
    name: "Login",
    data(){
        return {
            login: "kimziol",
            password: "Strong123",
            message: "",
        }
    },
    methods: {
        async getToken(){
            let url = 'http://localhost:8000/login'
            const fetchBody = {
                username: this.login,
                password: this.password
            }
            fetch(
                url, {
                    method: 'POST', 
                    mode: 'cors', 
                    cache: 'no-cache', 
                    credentials: 'same-origin', 
                    headers: {
                    'Content-Type': 'application/json'
                    },
                    redirect: 'follow', 
                    referrerPolicy: 'no-referrer', 
                    body: JSON.stringify(fetchBody)
                })
            .then(response => {
                if (response.status!==200){
                    this.message = response.statusText
                    throw new Error(response.statusText)
                }
                return response.json()
            })
            .then(data => this.$store.commit('updateToken', data))
            .then(() => this.$router.push({path: "/"}))
            .catch(err => console.error(err))
        },
    }
}
</script>

<style lang="scss" scoped>

</style>