<template>
    <div class="container-fluid">
        <h1>Product Categories</h1>
        <div v-if="message && message.detail" class="red lighten-4 red-text">{{ message.detail }}</div>
        <div>
            <button class="btn blue lighten-4 blue-text" data-bs-toggle="modal" :data-bs-target="'#createModal'">
                Create New Category
            </button>
            <div class="modal fade" :id="'createModal'" tabindex="-1" :aria-labelledby="'createModalLabel'" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" :id="'createModalLabel'">Create Category</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <product-category-form @category-update="refreshCategories($event)" :key="rebuild" :category-data="{category_name: '', root_category: null}" :categories-data="categories" :edit="false"></product-category-form>
                        </div>
                    </div>
                </div>
            </div>
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th scope="col">ID</th>
                            <th scope="col">Category</th>
                            <th scope="col">Group</th>
                            <th scope="col">Num. of Products</th>
                            <th scope="col">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="category in categories" :key="category.id">
                            <th scope="col">{{ category.id }}</th>
                            <td scope="col">{{ category.category_name }}</td>
                            <td scope="col">{{ (category.root_category) ? category.root_category.category_name : '-' }}</td>
                            <td scope="col">{{ category.products.length }}</td>
                            <td scope="col">
                                <button class="btn orange lighten-4 orange-text" data-bs-toggle="modal" :data-bs-target="'#editModal' + category.id">Edit</button>
                                <button class="btn red lighten-4 red-text ms-2" data-bs-toggle="modal" :data-bs-target="'#deleteModal' + category.id">Delete</button>
                            </td>
                            <div class="modal fade" :id="'editModal' + category.id" tabindex="-1" :aria-labelledby="'editModalLabel' + category.id" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" :id="'editModalLabel' + category.id">Edit Category</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <product-category-form @category-update="refreshCategories($event)" :key="rebuild" :category-data="category" :categories-data="categories" :edit="true"></product-category-form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="modal fade" :id="'deleteModal' + category.id" tabindex="-1" :aria-labelledby="'deleteModalLabel' + category.id" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" :id="'deleteModalLabel' + category.id">Delete Category</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            You are deleting <span class="blue-text">{{ category.category_name }}</span>
                                        </div>
                                        <div class="modal-footer">
                                            <button @click="deleteCategory(category.id)" type="button" class="btn btn-primary">Yes</button>
                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <pagination v-if="pages" :max="pages" @page-update="changePage($event)" :key="reload"></pagination>
    </div>
</template>

<script>
import Pagination from '../../components/Pagination.vue'
import ProductCategoryForm from '../../components/ProductCategoryForm.vue'
export default {
  components: { ProductCategoryForm, Pagination },
    data(){
        return {
            message: null,
            categories: null,
            rebuild: 1,
            pages: null,
            page: 1,
            reload: 0,
        }
    },
    methods: {
        async getCategories(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/product_categories/page/' + this.page, 'GET', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.categories = this.message.categories
                this.pages = this.message.pages
                this.message = null
                this.rebuild++
            }else{
                this.categories = []
            }
        },
        async deleteCategory(id){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/product_categories/' + id, 'DELETE', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.refreshCategories({id: id, action: 'DELETE'})
            }
        },
        refreshCategories(obj){ // action - edit, delete, create; id - category modal id
            if (obj.action == 'POST'){
                document.querySelector('#createModalLabel' + ' + button').click()
            }else if (obj.action == 'PUT'){
                document.querySelector('#editModalLabel' + obj.id + ' + button').click()
            }else if (obj.action == 'DELETE'){
                document.querySelector('#deleteModalLabel' + obj.id + ' + button').click()
            }
            this.getCategories()
        },
        changePage(page){
            this.page = page
            this.getCategories()
        }
    },
    computed: {
        
    },
    created(){
        this.getCategories()
    }
}
</script>