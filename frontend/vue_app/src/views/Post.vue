<template>
    <div class="container-fluid">
        <div class="row" v-if="post">
            <h1 class="col-12">{{ post.title }}</h1>
            <h5>Wrote by {{ post.author.username }}</h5>
            <h6>{{ new Date(post.date).toDateString() }}</h6>
            <p>{{ post.content }}</p>
            <h4>Comments:</h4>
            <ul>
                <li v-for="comment in post.comments" :key="comment.id">
                    {{ comment.content }}
                    <span class="blue-text">~ {{ comment.username + ' ' }}</span>
                    <span class="red-text">{{ new Date(comment.date).toDateString() }}</span>
                </li>
            </ul>
        </div>
        <div class="row" v-else>
            <h1>Post not found</h1>
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return {
            post: null
        }
    },
    methods: {
        async getPost(){
            this.post = await this.$fetchUtil(this.$store.getters.getUrl + "/posts/" + this.$route.params.id, 'GET', {}, this.$store.getters.getToken)
            console.log(this.post)
        }
    },
    created(){
        this.getPost()
    }
}
</script>

<style lang="scss">

</style>