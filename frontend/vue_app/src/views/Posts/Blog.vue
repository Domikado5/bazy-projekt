<template>
    <div>
        <h1>Blog</h1>
        <router-link :to="'/post/create'" v-show="$store.getters.getUser && $store.getters.getUser.role == 'writer'" class="btn blue darken-4 white-text text-lighten-4 mb-3 p-2">Create New Post</router-link>
        <div class="container-fluid px-4">
            <div class="row">
                <search-form type="Posts" @search-update="updateQuery($event)"></search-form>
            </div>
            <div class="row" v-if="posts && posts.length ==  0">
                <div class="col">
                    <h2>Not found</h2>
                </div>
            </div>
            <div class="row row-cols-1 row-cols-lg-3 row-cols-md-2 gy-4 gx-3">
                <div v-for="post in posts" :key="post.id" class="col">
                    <div class="card text-start blue-grey lighten-2 grey-text text-darken-4">
                        <div class="card-body">
                            <h5 class="card-title">{{ post.title }}</h5>
                        </div>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item blue-grey lighten-1">Author: {{ post.author.username }}</li>
                            <li class="list-group-item blue-grey lighten-1">Comments: {{ post.comments.length }}</li>
                            <li class="list-group-item blue-grey lighten-1">Date created: {{ new Date(post.date).toDateString() }}</li>
                        </ul>
                        <div class="card-body blue-grey darken-1">
                            <router-link :to="'/post/' + post.id" class="btn blue-grey darken-4 blue-grey-text text-lighten-4">Read post</router-link>
                            <router-link v-if="$store.getters.getUser && $store.getters.getUser.id == post.author.id" :to="'/post/edit/' + post.id" class="btn green darken-4 white-text ms-2">Edit Post</router-link>
                            <button v-if="$store.getters.getUser && $store.getters.getUser.id == post.author.id || $store.getters.getUser && $store.getters.getUser.role == 'admin'" class="btn red lighten-4 red-text ms-2" data-bs-toggle="modal" :data-bs-target="'#deleteModal' + post.id">Delete Post</button>
                            <div class="modal fade" :id="'deleteModal' + post.id" tabindex="-1" :aria-labelledby="'deleteModalLabel' + post.id" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" :id="'deleteModalLabel' + post.id">Delete Diary</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            You are deleting <span class="blue-text">{{ post.title }}</span>
                                        </div>
                                        <div class="modal-footer">
                                            <button v-if="$store.getters.getUser && $store.getters.getUser.id == post.author.id || $store.getters.getUser && $store.getters.getUser.role == 'admin'" @click="deletePost(post.id)" type="button" class="btn red lighten-4 red-text">Yes</button>
                                            <button type="button" class="btn green lighten-4 green-text" data-bs-dismiss="modal">No</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import SearchForm from '@/components/SearchForm.vue'
export default {
  components: { SearchForm },
    data(){
        return {
            posts: null,
        }
    },
    methods: {
        async getPosts(query){
            console.log("GET POST:")
            console.log(query)
            this.posts = await this.$fetchUtil(this.$store.getters.getUrl + '/posts/page/1', 'POST', query, this.$store.getters.getToken)
        },
        async deletePost(id){
            await this.$fetchUtil(this.$store.getters.getUrl + '/posts/' + id, 'DELETE', {}, this.$store.getters.getToken)
            document.querySelector('#deleteModalLabel' + id + ' + button').click()
            this.getPosts({title: '', sort: null})
        },
        updateQuery(q){
            const query = {
                title: q.search,
                sort: q.sort
            }
            console.log(q)
            this.getPosts(query)
        }
    },
    created(){
        this.getPosts({title: '', sort: null})
    }
}
</script>

<style lang="scss" scoped>
</style>