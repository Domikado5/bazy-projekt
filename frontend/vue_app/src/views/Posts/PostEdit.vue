<template>
    <div class="container-fluid">
    <h1>Edit Post</h1>
    <p v-if="message && message.detail" class="red-text red lighten-4 p-4">{{ message.detail }}</p>
    <div v-if="post">
        <post-form @send-data="updatePost($event)" post-button="Edit Post" :post-title="post.title" :post-content="post.content"></post-form>
    </div>
    </div>
</template>

<script>
import PostForm from "@/components/PostForm.vue"

export default {
    components: { PostForm },
    data(){
        return {
            post: null,
            message: null,
        }
    },
    methods: {
        async getPost(){
            this.post = await this.$fetchUtil(this.$store.getters.getUrl + '/posts/' + this.$route.params.id, 'GET', {}, this.$store.getters.getToken)
        },
        async updatePost(post){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/posts/' + this.$route.params.id, 'PUT', post, this.$store.getters.getToken)
            if (this.message && this.message.id){
                this.$router.push({path: "/post/" + this.message.id})
            }
        }
    },
    created(){
        this.getPost()
    }
}
</script>