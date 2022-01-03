<template>
    <form @submit.prevent="">
        <div class="mb-3">
            <label for="inputTitle" class="form-label">Title</label>
            <input type="text" id="inputTitle" class="form-control" v-model="title">
        </div>
        <div class="mb-3">
            <label for="inputContent" class="form-label">Content</label>
            <textarea id="inputContent" class="form-control" rows="5" v-model="content"></textarea>
        </div>
        <button class="btn blue accent-3" @click="sendData()">{{ postButton }}</button>
    </form>
</template>

<script>
export default {
    data() {
        return {
            title: this.postTitle,
            content: this.postContent,
            date: this.postDate,
            author: 0,
        }
    },
    props: {
        postButton: String,
        postTitle: String,
        postContent: String,
    },
    methods: {
        sendData(){
            let post = {
                'title': this.title,
                'content': this.content,
                'author': this.author
            }
            this.$emit('send-data', post)
        }
    }
}
</script>

<style lang="scss">

</style>