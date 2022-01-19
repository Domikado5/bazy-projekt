<template>
    <div class="container-fluid">
        <h1>Units</h1>
        <div v-if="message && message.detail" class="red lighten-4 red-text">{{ message.detail }}</div>
        <div class="row">
            <div>
                <button class="btn blue lighten-4 blue-text" data-bs-toggle="modal" :data-bs-target="'#createModal'">Create New Unit</button>
                <div class="modal fade" :id="'createModal'" tabindex="-1" :aria-labelledby="'createModalLabel'" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" :id="'createModalLabel'">Create Unit</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <unit-form @unit-update="refreshPage($event)" :unit-data="{id: null, unitname: ''}" :edit="false"></unit-form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th scope="col">ID</th>
                            <th scope="col">Unit</th>
                            <th scope="col">Num. of Products</th>
                            <th scope="col">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="unit in units" :key="unit.id">
                            <td scope="col">{{ unit.id }}</td>
                            <td scope="col">{{ unit.unitname }}</td>
                            <td scope="col">{{ unit.products.length }}</td>
                            <td scope="col">
                                <button class="btn orange lighten-4 orange-text" data-bs-toggle="modal" :data-bs-target="'#editModal' + unit.id">Edit</button>
                                <div class="modal fade" :id="'editModal' + unit.id" tabindex="-1" :aria-labelledby="'editModalLabel' + unit.id" aria-hidden="true">
                                    <div class="modal-dialog">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" :id="'editModalLabel' + unit.id">Edit Unit</h5>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <unit-form @unit-update="refreshPage($event)" :unit-data="unit" :edit="true"></unit-form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <button class="btn red lighten-4 red-text ms-2" data-bs-toggle="modal" :data-bs-target="'#deleteModal' + unit.id">Delete</button>
                                <div class="modal fade" :id="'deleteModal' + unit.id" tabindex="-1" :aria-labelledby="'deleteModalLabel' + unit.id" aria-hidden="true">
                                    <div class="modal-dialog">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" :id="'deleteModalLabel' + unit.id">Delete Unit</h5>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                You are deleting <span class="blue-text">{{ unit.unitname }}</span>
                                            </div>
                                            <div class="modal-footer">
                                                <button @click="deleteUnit(unit.id)" type="button" class="btn red lighten-4 red-text">Yes</button>
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
        <pagination v-if="pages" :max="pages" @page-update="changePage($event)" :key="reload"></pagination>
    </div>
</template>

<script>
import UnitForm from '@/components/UnitForm.vue'
import Pagination from '../../components/Pagination.vue'
export default {
    components: { UnitForm, Pagination },
    data(){
        return {
            message: null,
            units: null,
            page: 1,
            pages: null,
            reload: 0
        }
    },
    methods: {
        async getUnits(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/units/page/' + this.page, 'GET', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.units = this.message.units
                this.pages = this.message.pages
                this.message = null
            }
        },
        async deleteUnit(id){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/units/' + id, 'DELETE', {}, this.$store.getters.getToken)
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
            this.getUnits()
            this.reload++
            this.page = 1
        },
        changePage(page){
            this.page = page
            this.getUnits()
        }
    },
    created(){
        this.getUnits()
    }
}
</script>