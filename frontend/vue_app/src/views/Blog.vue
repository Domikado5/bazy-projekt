<template>
    <div>
        <h1>Blog</h1>
        <div class="container-fluid px-4">
            <div class="row row-cols-1 row-cols-lg-3 row-cols-md-2 gy-4 gx-3">
                <div v-for="post in posts" :key="post.id" class="col">
                    <div class="card text-start blue-grey lighten-2 grey-text text-darken-4">
                        <div class="card-body">
                            <h5 class="card-title">{{ post.title }}</h5>
                            <p class="card-text">{{ post.content }}</p>
                        </div>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item blue-grey lighten-1">Author: {{ post.author.username }}</li>
                            <li class="list-group-item blue-grey lighten-1">Comments: {{ post.comments.length }}</li>
                            <li class="list-group-item blue-grey lighten-1">Date created: {{ new Date(post.date).toDateString() }}</li>
                        </ul>
                        <div class="card-body blue-grey darken-1">
                            <router-link :to="'/post/' + post.id" class="btn blue-grey darken-4 blue-grey-text text-lighten-4">Read post: {{ post.id }}</router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return {
            posts: null
        }
    },
    methods: {
        async getPosts(){
            this.posts = await this.$fetchUtil(this.$store.getters.getUrl + '/posts/page/1', 'GET', {}, this.$store.getters.getToken)
        }
    },
    created(){
        this.getPosts()
    }
}
</script>

<style lang="scss" scoped>
</style>