<template>
    <form @submit.prevent="submitForm()">
        <div v-if="message && message.detail" class="red lighten-4 red-text ">
            {{ message.detail }}
        </div>
        <div class="mb-3">
            <label for="inputCategory" class="form-label">Category Name</label>
            <input required type="text" id="inputCategory" class="form-control" v-model="category.category_name">
        </div>
        <div class="mb-3">
            <button v-if="edit == true" class="btn orange lighten-4 orange-text">Edit</button>
            <button v-if="edit == false" class="btn blue lighten-4 blue-text">Create</button>
        </div>
    </form>
</template>

<script>
export default {
    data(){
        return {
            message: null,
            id: this.categoryData.id,
            category: {
                category_name: this.categoryData.category_name
            }
        }
    },
    props: {
        categoryData: Object,
        edit: Boolean
    },
    methods: {
        async submitForm(){
            const method = (this.edit == true) ? 'PUT' : 'POST'
            const endpoint = (this.id) ? '/set_categories/' + this.id : '/set_categories'
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + endpoint, method, this.category, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.$emit('categoryUpdate', {id: this.message.id, action: method})
            }
        }
    }
}
</script>