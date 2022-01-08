<template>
    <div class="container-fluid">
        <h1>Allergens</h1>
        <div class="red lighten-4 red-text" v-if="message && message.detail">{{ message.detail }}</div>
        <div class="row">
            <div>
                <button class="btn blue lighten-4 blue-text" data-bs-toggle="modal" :data-bs-target="'#createModal'">Create Allergen</button>
                <div class="modal fade" :id="'createModal'" tabindex="-1" :aria-labelledby="'createModalLabel'" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" :id="'createModalLabel'">Create Allergen</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <allergen-form @allergen-update="refreshPage($event)" :allergen-data="{id: null, allergen: ''}" :edit="false"></allergen-form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th scope="col">ID</th>
                            <th scope="col">Allergen</th>
                            <th scope="col">Num. of Products</th>
                            <th scope="col">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="allergen in allergens" :key="allergen.id">
                            <th scope="col">{{ allergen.id }}</th>
                            <td scope="col">{{ allergen.allergen }}</td>
                            <td scope="col">{{ allergen.products.length }}</td>
                            <td scope="col">
                                <button class="btn orange lighten-4 orange-text" data-bs-toggle="modal" :data-bs-target="'#editModal' + allergen.id">Edit</button>
                                <button class="btn red lighten-4 red-text ms-2" data-bs-toggle="modal" :data-bs-target="'#deleteModal' + allergen.id">Delete</button>
                            </td>
                            <div class="modal fade" :id="'editModal' + allergen.id" tabindex="-1" :aria-labelledby="'editModalLabel' + allergen.id" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" :id="'editModalLabel' + allergen.id">Edit Allergen</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <allergen-form @allergen-update="refreshPage($event)" :allergen-data="allergen" :edit="true"></allergen-form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="modal fade" :id="'deleteModal' + allergen.id" tabindex="-1" :aria-labelledby="'deleteModalLabel' + allergen.id" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" :id="'deleteModalLabel' + allergen.id">Delete Allergen</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            You are deleting <span class="blue-text">{{ allergen.allergen }}</span>
                                        </div>
                                        <div class="modal-footer">
                                            <button @click="deleteAllergen(allergen.id)" type="button" class="btn red lighten-4 red-text">Yes</button>
                                            <button type="button" class="btn green lighten-4 green-text" data-bs-dismiss="modal">No</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import AllergenForm from '@/components/AllergenForm.vue'
export default {
    components: { AllergenForm },
    data(){
        return {
            message: null,
            allergens: null
        }
    },
    methods: {
        async getAllergens(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/allergens/page/' + this.$route.params.page, 'GET', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.allergens = this.message
                this.message == null
            }
        },
        async deleteAllergen(id){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/allergens/' + id, 'DELETE', {}, this.$store.getters.getToken)
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
            this.getAllergens()
        }
    },
    created(){
        this.getAllergens()
    }
}
</script>