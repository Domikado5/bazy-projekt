<template>
    <div class="container-fluid">
        <h1>Users List - Page {{ $route.params.page }}</h1>
        <h3 class="red lighten-4 red-text" v-if="message && message.detail">{{ message.detail }}</h3>
        <div>
            <search-form @search-update="updateQuery($event)" type="Users"></search-form>
        </div>
        <div class="table-responsive">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Username</th>
                    <th scope="col">Role</th>
                    <th scope="col">Email</th>
                    <th scope="col">Posts</th>
                    <th scope="col">Diaries</th>
                    <th scope="col">Sets</th>
                    <th scope="col">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr class="" v-for="user in users" :key="user.id">
                    <th>{{ user.id }}</th>
                    <td>{{ user.username }}</td>
                    <td><span class="badge" :class="{'blue': user.role=='user', 'green': user.role=='writer', 'purple': user.role=='admin'}">{{ user.role }}</span></td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.posts.length }}</td>
                    <td>{{ user.diaries.length }}</td>
                    <td>{{ user.sets.length }}</td>
                    <td>
                        <button class="btn orange me-2 yellow-text text-lighten-5" data-bs-toggle="modal" :data-bs-target="'#userEditModal' + user.id">Edit</button>
                        <button class="btn red pink-text text-lighten-5" data-bs-toggle="modal" :data-bs-target="'#deleteModal' + user.id">Delete</button>
                    </td>
                    <div class="modal fade" :id="'deleteModal' + user.id" tabindex="-1" :aria-labelledby="'deleteModalLabel' + user.id" aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" :id="'deleteModalLabel' + user.id">Are you sure?</h5>
                                    <button type="button" :id="'deleteModalClose' + user.id" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    You are deleting <span class="blue-text">{{ user.username }}</span>
                                </div>
                                <div class="modal-footer">
                                    <button @click="deleteUser(user.id)" type="button" class="btn red lighten-4 red-text">Yes</button>
                                    <button type="button" class="btn green lighten-4 green-text" data-bs-dismiss="modal">No</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal fade" :id="'userEditModal' + user.id" tabindex="-1" :aria-labelledby="'userModalLabel' + user.id" aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" :id="'userModalLabel' + user.id">Edit User Data</h5>
                                    <button type="button" :id="'userEditModalClose' + user.id" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <user-form @user-update="refreshUser(user.id)" :user-id="user.id" :user-username="user.username" :user-email="user.email" :user-role="user.role"></user-form>
                                </div>
                            </div>
                        </div>
                    </div>
                </tr>
            </tbody>
        </table>
        </div>
        <pagination v-if="pages" :max="pages" @page-update="changePage($event)" :key="reload"></pagination>
    </div>
</template>

<script>
import UserForm from '@/components/UserForm.vue'
import SearchForm from '@/components/SearchForm.vue'
import Pagination from '../../components/Pagination.vue'


export default {
  components: { UserForm, SearchForm, Pagination },
    data(){
        return {
            users: null,
            message: null,
            query: {
                username: null,
                role: null,
                sort: null,
            },
            pages: null,
            page: 1,
            reload: 0
        }
    },
    methods: {
        async getUsers(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/users/page/' + this.page, 'POST', this.query, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.users = this.message.users
                this.pages = this.message.pages
                this.message = null
            }
        },
        refreshUser(id){
            document.querySelector("#userEditModalClose" + id).click()
            this.getUsers()
            this.reload++
            this.page = 1
        },
        async deleteUser(id){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/users/' + id, 'DELETE', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                if (id == this.$store.getters.getUser.id){
                    this.$store.commit('resetToken')
                    this.$router.push({path: "/"})
                }else{
                    document.querySelector("#deleteModalClose" + id).click()
                    this.getUsers()
                    this.reload++
                    this.page = 1
                }
            }
        },
        updateQuery(q){
            this.query = {
                username: q.search,
                role: q.role,
                sort: q.sort,
            }
            console.log(q)
            this.getUsers()
            this.reload++
            this.page = 1
        },
        changePage(page){
            this.page = page
            this.getUsers()
        }
    },
    created(){
        this.getUsers()
    }
}
</script>