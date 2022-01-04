<template>
    <form @submit.prevent="updateUser()">
        <div v-if="message && message.detail" class="red lighten-4 red-text ">
            {{ message.detail }}
        </div>
        <div class="mb-3">
            <label for="inputUsername" class="form-label">Username</label>
            <input type="text" id="inputUsername" class="form-control" v-model="user.username">
        </div>
        <div class="mb-3">
            <label for="inputEmail" class="form-label">Email</label>
            <input type="email" id="inputEmail" class="form-control" v-model="user.email">
        </div>
        <div class="mb-3" v-if="$store.getters.getUser && $store.getters.getUser.id != id && $store.getters.getUser.role == 'admin'">
            <label for="selectRole" class="form-label">Role</label>
            <select class="form-select" id="selectRole" v-model="user.role">
                <option :selected="userRole == 'user'" value="user">User</option>
                <option :selected="userRole == 'writer'" value="writer">Writer</option>
                <option :selected="userRole == 'admin'" value="admin">Admin</option>
            </select>
        </div>
        <div class="mb-3" v-else>
            <label for="inputPassword" class="form-label">Password</label>
            <input type="password" id="inputPassword" class="form-control" v-model="user.password">
        </div>
        <button class="btn purple accent-3 pink-text text-lighten-5">Update User Data</button>
    </form>
</template>

<script>
export default {
    data(){
        return {
            id: this.userId,
            user: {
                username: this.userUsername,
                email: this.userEmail,
                role: this.userRole,
                password: null
            },
            message: null
        }
    },
    props: {
        userId: Number,
        userUsername: String,
        userEmail: String,
        userRole: String
    },
    methods: {
        async updateUser(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/users/' + this.id, 'PUT', this.user, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.$emit('userUpdate')
            }
        }
    }
}
</script>