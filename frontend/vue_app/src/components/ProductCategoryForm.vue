<template>
    <form @submit.prevent="resolveCategory">
        <div v-if="message && message.detail" class="red lighten-4 red-text ">
            {{ message.detail }}
        </div>
        <div class="mb-3 col-12">
            <label for="inputCategoryName" class="form-label">Category Name</label>
            <input required type="text" id="inputCategoryName" class="form-control" v-model="category.category_name">
        </div>
        <div class="mb-3 col-12">
            <label for="inputRootCategory" class="form-label">Root Category</label>
            <select id="inputRootCategory" class="form-select" v-model="category.root_category">
                <option v-for="cat in noRepeat" :selected="category.root_category && cat.id == category.root_category.id" :key="cat.id" :value="cat.id">{{ cat.category_name }}</option>
            </select>
        </div>
        <div class="mb-3 col-12">
            <button v-if="edit == true" class="btn orange lighten-4 orange-text">Edit Category</button>
            <button v-else class="btn blue lighten-4 blue-text">Create Category</button>
        </div>
    </form>
</template>

<script>
export default {
    data(){
        return {
            message: null,
            id: this.categoryData.id,
            categories: this.categoriesData,
            category: {
                category_name: this.categoryData.category_name,
                root_category: (this.categoryData.root_category) ? this.categoryData.root_category.id : null
            }
        }
    },
    props: {
        categoryData: Object,
        categoriesData: Array,
        edit: Boolean
    },
    methods: {
        async resolveCategory(){
            const method = (this.edit == true) ? 'PUT' : 'POST'
            const endpoint = (this.id) ? '/product_categories/' + this.id : '/product_categories'
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + endpoint, method, this.category, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.$emit('categoryUpdate', {id: this.message.id, action: method})
            }
        }
    },
    computed: {
        noRepeat() {
            if (this.categories)return this.categories.filter(cat => cat.id != this.id)
            return []
        }
    },
    created(){
        
    }
}
</script>