<template>
    <div class="container-fluid">
        <h1>Create New Post</h1>
        <p v-if="message && message.detail" class="red-text red lighten-4 p-4">{{ message.detail }}</p>
        <post-form @send-data="getPostData($event)" post-button="Create Post" post-title="" post-content=""></post-form>
    </div>
</template>

<script>
import PostForm from "@/components/PostForm.vue"

export default {
    components: { PostForm },
    data() {
        return {
            message: null
        }
    },
    methods: {
        async getPostData(post){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/posts/', 'POST', post, this.$store.getters.getToken)
            if (this.message && this.message.id){
                this.$router.push({path: "/post/" + this.message.id})
            }
        }
    }
}
</script>

<style lang="scss">

</style>