<template>
    <div class="container-fluid">
        <div class="row">
            <h1>Diary</h1>
            <div class="red lighten-4 red-text" v-if="message && message.detail">{{ message.detail }}</div>
        </div>
        <div class="row" v-if="diary">
            <h2>{{ diary.date }}</h2>
            <div class="col-12 mb-3">
                <button class="btn orange text-lighten-5 orange-text" data-bs-toggle="modal" :data-bs-target="'#editModal' + diary.id">Edit</button>
                <div class="modal fade" :id="'editModal' + diary.id" tabindex="-1" :aria-labelledby="'editModalLabel' + diary.id" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" :id="'editModalLabel' + diary.id">Edit diary</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <diary-form @diary-update="refreshPage($event)" :diary-data="diary" :edit="true"></diary-form>
                            </div>
                        </div>
                    </div>
                </div>
                <button class="btn red text-lighten-5 red-text ms-2" data-bs-toggle="modal" :data-bs-target="'#deleteModal' + diary.id"><i class="bi bi-trash-fill"></i></button>
                <div class="modal fade" :id="'deleteModal' + diary.id" tabindex="-1" :aria-labelledby="'deleteModalLabel' + diary.id" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" :id="'deleteModalLabel' + diary.id">Delete Diary</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                You are deleting <span class="blue-text">{{ diary.date }}</span>
                            </div>
                            <div class="modal-footer">
                                <button @click="deleteDiary()" type="button" class="btn red lighten-4 red-text">Yes</button>
                                <button type="button" class="btn green lighten-4 green-text" data-bs-dismiss="modal">No</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-12">
                    <h5>Fats: {{ diary.total_fats }}</h5>
                    <h5>Proteins: {{ diary.total_proteins }}</h5>
                    <h5>Carbs: {{ diary.total_carbohydrates }}</h5>
                    <h5>Calories: {{ diary.total_calories }}</h5>
            </div>
            <div class="col-12">
                <h3>Entries:</h3>
                <div class="row">
                    <div class="col-12 py-1" v-for="entry in diary.entries" :key="entry.id">
                        {{ entry.product_id.product_name }} : {{ entry.amount }}{{ entry.product_id.unit.unitname }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import DiaryForm from '@/components/DiaryForm.vue'
export default {
  components: { DiaryForm },
    data(){
        return {
            message: null,
            diary: null
        }
    },
    methods: {
        async getDiary(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/diaries/' + this.$route.params.id, 'GET', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.diary = this.message.diary
                this.diary.entries = this.message.entries
                this.message = null
            }
        },
        async deleteDiary(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/diaries/' + this.$route.params.id, 'DELETE', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.refreshPage({id: this.$route.params.id, action: 'DELETE', close: true})
            }
        },
        refreshPage(obj){
            if (obj.close == true){
                if (obj.action == 'POST'){
                    document.querySelector('#createModalLabel' + ' + button').click()
                }else if (obj.action == 'PUT'){
                    document.querySelector('#editModalLabel' + obj.id + ' + button').click()
                }else if (obj.action == 'DELETE'){
                    document.querySelector('#deleteModalLabel' + obj.id + ' + button').click()
                    this.$router.push("/diaries/1")
                }
            }
            this.getDiary()
        }
    },
    created(){
        this.getDiary()
    }
}
</script>