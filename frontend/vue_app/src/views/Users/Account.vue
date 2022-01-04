<template>
    <div class="container-fluid">
        <div class="row">
            <h3 v-if="message && message.detail" class="red-text red lighten-4 p-4">{{ message.detail }}</h3>
        </div>
        <div class="row" v-if="user">
            <h1>Your account</h1>
            <h4>{{ user.username }} <span v-if="user.role != 'user'" class="badge rounded-pill purple">{{ user.role }}</span></h4>
            <h5>{{ user.email }}</h5>
            <div v-if="user.role == 'writer'" class="my-1">
                <h5>Your posts <span class="badge rounded-pill green white-text">{{ user.posts.length }}</span></h5>
                <router-link class="btn purple accent-3 white-text" v-for="post in user.posts" :key="post.id" :to="'/post/'+post.id">{{ post.title }}</router-link>
            </div>
            <div class="my-1">
                <h5>Your diaries <span class="badge rounded-pill green white-text">{{ user.diaries.length }}</span></h5>
                <a href="#" v-for="diary in user.diaries" :key="diary.id" class="btn purple accent-4 white-text">{{ diary.date }}</a>
            </div>
            <div class="my-1">
                <h5>Your sets <span class="badge rounded-pill green white-text">{{ user.sets.length }}</span></h5>
                <a href="#" v-for="set in user.sets" :key="set.id" class="btn purple accent-4 white-text">{{ set.set_name }}</a>
            </div>
            <div class="my-1" v-if="$store.getters.getUser.role == 'admin' || $store.getters.getUser.id == user.id">
                <button @click="deleteUser()" class="btn red accent-2 text-white mx-1">Delete Account</button>
                <button class="btn orange accent-2 text-white" data-bs-toggle="modal" data-bs-target="#userEditModal">Update Account</button>
            </div>
            <div class="modal fade" id="userEditModal" tabindex="-1" aria-labelledby="userModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="userModalLabel">Edit User Data</h5>
                            <button type="button" id="userEditModalClose" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <user-form @user-update="refreshUser()" :user-id="user.id" :user-username="user.username" :user-email="user.email"></user-form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import UserForm from '@/components/UserForm.vue'

export default {
  components: { UserForm },
    data(){
        return {
            user: null,
            message: null,
        }
    },
    methods: {
        async getUser(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/users/' + this.$route.params.id, 'GET', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.user = this.message
            }
        },
        async deleteUser(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/users/' + this.$route.params.id, 'DELETE', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                if (this.user.id == this.$store.getters.getUser.id){
                    this.$store.commit('resetToken')
                    this.$router.push({path: "/"})
                }
            }
        },
        refreshUser(){
            document.querySelector("#userEditModalClose").click()
            this.getUser()
        }
    },
    created(){
        this.getUser()
    }
}
</script>