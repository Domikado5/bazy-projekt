<template>
    <div class="container-fluid">
        <div class="row justify-content-center" v-if="post">
            <h1 class="col-12">{{ post.title }}</h1>
            <div class="mb-2">

            <router-link v-if="$store.getters.getUser && $store.getters.getUser.id == post.author.id" :to="'/post/edit/' + post.id" class="btn green darken-4 white-text ms-2">Edit Post</router-link>
            <button v-if="($store.getters.getUser && $store.getters.getUser.id == post.author.id) || $store.getters.getUser && $store.getters.getUser.role == 'admin'" class="btn red darken-3 white-text ms-2" @click="deletePost(post.id)">Delete Post</button>
            </div>
            <h5>Wrote by {{ post.author.username }}</h5>
            <h6>{{ new Date(post.date).toDateString() }}</h6>
            <p>{{ post.content }}</p>
            <h4>Comments:</h4>
            <p v-if="message && message.detail" class="red-text red lighten-4 p-4">{{ message.detail }}</p>
            <form @submit.prevent="sendComment()" class="d-flex justify-content-center" v-show="$store.getters.getUser">
                <div class="input-group mb-3">
                    <input type="text" id="inputComment" class="form-control" v-model="comment">
                    <button class="btn blue accent-1">Send comment</button>
                </div>
            </form>
            <div>
                <search-form @search-update="updateQuery($event)" type="Comments"></search-form>
            </div>
            <div v-if="post.comments && post.comments.length == 0">
                <h2>No comments</h2>
            </div>
            <ul class="d-flex flex-column justify-content-center col-12 col-lg-6">
                <li v-for="comment in post.comments" :key="comment.id" class="mb-2 d-flex justify-content-end blue lighten-4 p-2">
                    <form class="" @submit.prevent="updateComment(comment.id)" v-show="commentsEdit.filter(element => {return element.id == comment.id})[0].edit">
                        <div class="input-group">
                            <input type="text" v-model="commentsEdit.filter(element => {return element.id == comment.id})[0].comment">
                            <button class="btn green lighten-4"><i class="bi bi-check2"></i></button>
                        </div>
                    </form>
                    <span class="" v-show="! commentsEdit.filter(element => {return element.id == comment.id})[0].edit">{{ getCommentContent(comment.id) }}</span>
                    <span class="blue-text mx-1">~ {{ comment.username + ' ' }}</span>
                    <span class="red-text mx-1">{{ new Date(comment.date).toLocaleString() }}</span>
                    <button @click="toggleEdit(comment.id)" v-if="this.$store.getters.getUser && comment.username == this.$store.getters.getUser.username" class="btn grey lighten-2 grey-text text-darken-2 py-1 px-2 ms-2"><i class="bi bi-pencil-square"></i></button>
                    <button data-bs-toggle="modal" :data-bs-target="'#deleteModal' + comment.id" v-if="this.$store.getters.getUser && (post.author.id == this.$store.getters.getUser.id || this.$store.getters.getUser.role == 'admin' || comment.username == this.$store.getters.getUser.username)" class="btn red lighten-2 red-text text-darken-2 py-1 px-2 ms-2"><i class="bi bi-trash-fill"></i></button>
                    <div class="modal fade" :id="'deleteModal' + comment.id" tabindex="-1" :aria-labelledby="'deleteModalLabel' + comment.id" aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" :id="'deleteModalLabel' + comment.id">Delete Diary</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    You are deleting <span class="blue-text">{{ comment.content }}</span>
                                </div>
                                <div class="modal-footer">
                                    <button @click="deleteComment(comment.id)" type="button" class="btn red lighten-4 red-text">Yes</button>
                                    <button type="button" class="btn green lighten-4 green-text" data-bs-dismiss="modal">No</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
        <div class="row" v-else>
            <h1>Post not found</h1>
        </div>
    </div>
</template>

<script>
import SearchForm from '@/components/SearchForm.vue';
export default {
  components: { SearchForm },
    data(){
        return {
            post: null,
            comment: null,
            message: null,
            commentsEdit: [],
            query: {
                sort: '-date'
            }
        }
    },
    methods: {
        async getPost(){
            this.post = await this.$fetchUtil(this.$store.getters.getUrl + "/posts/" + this.$route.params.id, 'GET', {}, this.$store.getters.getToken)
            this.getComments()
            this.post.comments.forEach(comment => {
                this.commentsEdit.push({'id': comment.id, 'edit': false, 'comment': comment.content})
            })
        },
        async deletePost(id){
            await this.$fetchUtil(this.$store.getters.getUrl + '/posts/' + id, 'DELETE', {}, this.$store.getters.getToken)
            this.$router.push({path: "/blog"})
        },
        async sendComment(){
            let today = new Date();
            let date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate()+' '+today.getHours()+':'+today.getMinutes()+':'+today.getSeconds();
            let comment = {
                "username": this.$store.getters.getUser.username,
                "content": this.comment,
                "date": date,
                "root_post": parseInt(this.$route.params.id)
            }
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/comments', 'POST', comment, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.getPost()
            }
        },
        async deleteComment(id){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/comments/' + id, 'DELETE', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                document.querySelector('#deleteModalLabel' + id + ' + button').click()
                this.getPost()
            }
        },
        async getComments(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/comments/' + this.post.id + '/page/1', 'POST', this.query, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.post.comments = this.message
                console.log("Comments sorted")
            }
        },
        toggleEdit(id){
            this.commentsEdit.forEach(element => {
                if (element.id == id){
                    element.edit = !element.edit
                }
            })
        },
        updateComment(id){
            this.commentsEdit.forEach(async element => {
                if (element.id == id){
                    let comment = {
                        "content": element.comment
                    }
                    this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/comments/' + id, 'PUT', comment, this.$store.getters.getToken)
                    if (this.message && !this.message.detail){
                        this.post.comments.forEach(comm => {
                            if (comm.id == id){
                                comm.content = element.comment
                            }
                        })
                        element.edit = !element.edit
                    }
                }
            })
        },
        getCommentContent(id){
            let res = ""
            for (let i=0; i < this.post.comments.length; i++) {
                let comment = this.post.comments[i]
                if (comment.id == id) {
                    res = comment.content
                    break
                }
            }
            return res
        },
        updateQuery(q){
            this.query = {
                sort: q.sort
            }
            this.getComments()
        }
    },
    created(){
        this.getPost()
    }
}
</script>

<style lang="scss">
</style>