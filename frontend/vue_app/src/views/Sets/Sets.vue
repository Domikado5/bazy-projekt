<template>
    <div class="container-fluid">
        <div class="row">
        <h1>Your sets</h1>
        <div class="red lighten-4 red-text" v-if="message && message.detail">{{ message.detail }}</div>
        </div>
        <div class="row">
            <div class="col-12">
                <button class="btn blue lighten-4 blue-text" data-bs-toggle="modal" :data-bs-target="'#createModal'">Create New Set</button>
                <div class="modal fade" :id="'createModal'" tabindex="-1" :aria-labelledby="'createModalLabel'" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" :id="'createModalLabel'">Create Set</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <set-form @set-update="refreshPage($event)" :set-data="{id: null, set_name: '', description: '', products: [], categories: null}" :edit="false" :key="reload" :categories-data="categories"></set-form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-for="set in sets" :key="set.id" class="col-12 col-lg-6 mt-3">
                <div class="card blue accent-1 p-0 card-border">
                <h3 class="card-header blue accent-2">
                    {{ set.set_name }}
                </h3>
                <div class="card-body black-text">
                    <p class="card-text black-text">{{ set.description }}</p>
                    <h5 class="m-0">Products:</h5>
                </div>
                <div class="blue darken-2" style="height: 150px; max-height: 150px; overflow-y:scroll;">
                    <div v-for="product in set.products" :key="product.id" class="blue darken-2 mt-1">
                        <div class="d-flex justify-content-center black-text">
                            <div class="">{{ product.product_name }}:</div>
                            <div class="ms-2">{{ product.calories }} kcal</div>
                        </div>
                    </div>
                </div>
                <div class="card-body black-text">
                    <h5 class="m-0">Categories:</h5>
                    <div class="d-flex justify-content-evenly">
                        <div v-for="category in set.categories" :key="category.id" class="badge purple darken-4 p-2">{{ category.category_name }}</div>
                    </div>
                </div>
                <div class="card-footer blue accent-2">
                    <button class="btn orange lighten-4 orange-text me-1" data-bs-toggle="modal" :data-bs-target="'#editModal' + set.id">Edit</button>
                    <div class="modal fade" :id="'editModal' + set.id" tabindex="-1" :aria-labelledby="'editModalLabel' + set.id" aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" :id="'editModalLabel' + set.id">Edit Set</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <set-form @set-update="refreshPage($event)" :set-data="set" :edit="true" :key="reload" :categories-data="categories"></set-form>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button class="btn red lighten-4 red-text ms-1" data-bs-toggle="modal" :data-bs-target="'#deleteModal' + set.id">Delete</button>
                    <div class="modal fade" :id="'deleteModal' + set.id" tabindex="-1" :aria-labelledby="'deleteModalLabel' + set.id" aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" :id="'deleteModalLabel' + set.id">Delete Set</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-footer">
                                    <button @click="deleteSet(set.id)" type="button" class="btn red lighten-4 red-text">Yes</button>
                                    <button type="button" class="btn green lighten-4 green-text" data-bs-dismiss="modal">No</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import SetForm from '@/components/SetForm.vue'
export default {
  components: { SetForm },
    data(){
        return {
            message: null,
            sets: null,
            categories: null,
            reload: 1
        }
    },
    methods: {
        async getSets(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/sets/page/' + this.$route.params.page, 'GET', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.sets = this.message
                this.message = null
                this.reload++
            }
        },
        async deleteSet(id){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/sets/' + id, 'DELETE', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.refreshPage({id: id, action: 'DELETE'})
            }
        },
        async getCategories(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/set_categories', 'GET', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.categories = this.message
                this.message = null
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
            this.getSets()
        }
    },
    created(){
        this.getCategories()
        this.getSets()
    }
}
</script>

<style lang="scss" scoped>
    div.card-border{
        border: 5px solid #0d47a1;
    }
</style>