<template>
    <div class="container-fluid">
        <div class="row">
            <h1>Set Categories</h1>
            <div v-if="message && message.detail">
                {{ message.detail }}
            </div>
            <div>
                <button class="btn blue lighten-4 blue-text" data-bs-toggle="modal" :data-bs-target="'#createModal'">Create New Category</button>
                <div class="modal fade" :id="'createModal'" tabindex="-1" :aria-labelledby="'createModalLabel'" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" :id="'createModalLabel'">Create Category</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <set-category-form @category-update="refreshPage($event)" :category-data="{id: null, category_name: ''}" :edit="false"></set-category-form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row table-resposive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">ID</th>
                        <th scope="col">Name</th>
                        <th scope="col">Num. of Sets</th>
                        <th scope="col">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="category in categories" :key="category.id">
                        <th scope="col">{{ category.id }}</th>
                        <td scope="col">{{ category.category_name }}</td>
                        <td scope="col">{{ category.sets.length }}</td>
                        <td scope="col">
                            <button class="btn orange lighten-4 orange-text" data-bs-toggle="modal" :data-bs-target="'#editModal' + category.id">Edit</button>
                            <div class="modal fade" :id="'editModal' + category.id" tabindex="-1" :aria-labelledby="'editModalLabel' + category.id" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" :id="'editModalLabel' + category.id">Edit Category</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <set-category-form @category-update="refreshPage($event)" :category-data="category" :edit="true"></set-category-form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <button class="btn red lighten-4 red-text ms-2" data-bs-toggle="modal" :data-bs-target="'#deleteModal' + category.id">Delete</button>
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
                                            <button @click="deleteCategory(category.id)" type="button" class="btn red lighten-4 red-text">Yes</button>
                                            <button type="button" class="btn green lighten-4 green-text" data-bs-dismiss="modal">No</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import SetCategoryForm from '@/components/SetCategoryForm.vue'
export default {
  components: { SetCategoryForm },
    data(){
        return {
            message: null,
            categories: null
        }
    },
    methods: {
        async getCategories(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/set_categories', 'GET', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.categories = this.message
                this.message = null
            }
        },
        async deleteCategory(id){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/set_categories/' + id, 'DELETE', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.refreshPage({id: id, action: 'DELETE'})
            }
        },
        refreshPage(obj){
            if (obj.action == 'POST'){
                document.querySelector('#createModalLabel' + ' + button').click()
            }else if (obj.action == 'PUT'){
                document.querySelector('#editModalLabel' + obj.id + ' + button').click()
            }else if (obj.action == 'DELETE'){
                document.querySelector('#deleteModalLabel' + obj.id + ' + button').click()
            }
            this.getCategories()
        }
    },
    created(){
        this.getCategories()
    }
}
</script>