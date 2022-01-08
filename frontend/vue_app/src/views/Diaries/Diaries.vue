<template>
    <div class="container-fluid">
        <div class="row">
            <h1>Diaries</h1>
            <div>
                <button class="btn blue lighten-4 blue-text" data-bs-toggle="modal" :data-bs-target="'#createModal'">Add New Diary</button>
                <div class="modal fade" :id="'createModal'" tabindex="-1" :aria-labelledby="'createModalLabel'" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" :id="'createModalLabel'">Create Diary</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <form @submit.prevent="createDiary()">
                                    <div v-if="formMessage && formMessage.detail" class="red lighten-4 red-text ">
                                        {{ formMessage.detail }}
                                    </div>
                                    <div class="mb-3">
                                        <label for="inputDate" class="form-label">Date</label>
                                        <input required type="date" id="inputDate" class="form-control" v-model="date">
                                    </div>
                                    <div class="mb-3">
                                        <button class="btn blue lighten-4 blue-text">Create</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="red lighten-4 red-text" v-if="message && message.detail">{{ message.detail }}</div>
        </div>
        <div class="row my-3">
            <search-form @search-update="refrshPage($event)" type="Diaries" :dateData="new Date()"></search-form>
        </div>
        <div class="row" v-if="diaries && diaries.length == 0">
            <h2>Diaries not found</h2>
        </div>
        <div class="row">
            <div v-for="diary in diaries" :key="diary.id" class="col-12 col-lg-4">
                <div class="card">
                    <div class="card-header blue white-text">
                        <h5 class="card-title m-0">{{ diary.date }}</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <h4 class="col-12">You ate:</h4>
                            <div class="col-6 orange-text text-end">
                                Fats: {{ diary.total_fats }} g
                            </div>
                            <div class="col-6 blue-text text-start">
                                Proteins: {{ diary.total_proteins }} g
                            </div>
                            <div class="col-6 green-text text-end">
                                Carbs: {{ diary.total_carbohydrates }} g
                            </div>
                            <div class="col-6 purple-text text-start">
                                Calories: {{ diary.total_calories }} kcal
                            </div>
                        </div>
                        <div class="mt-2">
                            <router-link :to="'/diary/' + diary.id" class="btn blue text-lighten-5 blue-text">Show</router-link>
                            <button class="btn red text-lighten-5 red-text ms-2" data-bs-toggle="modal" :data-bs-target="'#deleteModal' + diary.id"><i class="bi bi-trash-fill"></i></button>
                            <div class="modal fade" :id="'deleteModal' + diary.id" tabindex="-1" :aria-labelledby="'deleteModalLabel' + diary.id" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" :id="'deleteModalLabel' + diary.id">Delete Diary</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            {{ diary.date }}
                                        </div>
                                        <div class="modal-footer">
                                            <button @click="deleteDiary(diary.id)" type="button" class="btn red lighten-4 red-text">Yes</button>
                                            <button type="button" class="btn green lighten-4 green-text" data-bs-dismiss="modal">No</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer blue lighten-4">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import SearchForm from '../../components/SearchForm.vue'

const today = new Date()
const day = (today.getDate() < 10) ? ('0' + today.getDate()) : today.getDate()
const month = (today.getMonth()+1 < 10) ? ('0' + (today.getMonth()+1)) : (today.getMonth()+1)
const year = today.getFullYear()

export default {
  components: { SearchForm },
    data(){
        return {
            message: null,
            diaries: null,
            date: year + '-' + month + '-' + day,
            formMessage: null
        }
    },
    methods: {
        async getDiaries(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/diaries/date/' + this.date, 'GET', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.diaries = this.message
                this.message = null
                this.diaries.forEach(obj => {
                    obj.diary.entries = obj.entries
                    delete obj.entries
                })
                this.diaries = this.diaries.map(({diary}) => diary)
            }else{
                this.diaries = null
            }
        },
        async deleteDiary(id){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/diaries/' + id, 'DELETE', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                document.querySelector('#deleteModalLabel' + id + ' + button').click()
                this.getDiaries()
            }
        },
        async createDiary(){
            const diary = {
                date: this.date,
                total_calories: 0,
                total_fats: 0,
                total_proteins: 0,
                total_carbohydrates: 0,
                owner: 0
            }
            this.formMessage = await this.$fetchUtil(this.$store.getters.getUrl + '/diaries', 'POST', diary, this.$store.getters.getToken)
            if (this.formMessage && !this.formMessage.detail){
                document.querySelector('#createModalLabel' + ' + button').click()
                this.$router.push("/diary/" + this.formMessage.id)
            }
        },
        refrshPage(obj){
            const today = obj.date
            const day = (today.getDate() < 10) ? ('0' + today.getDate()) : today.getDate()
            const month = (today.getMonth()+1 < 10) ? ('0' + (today.getMonth()+1)) : (today.getMonth()+1)
            const year = today.getFullYear()
            this.date =  year + '-' + month + '-' + day
            this.getDiaries()
        }
    },
    created(){
        this.getDiaries()
    }
}
</script>