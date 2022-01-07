<template>
    <form @submit.prevent="">
        <div v-if="message && message.detail" class="red lighten-4 red-text ">
            {{ message.detail }}
        </div>
        <div class="mb-3">
            <label for="inputDate" class="form-label">Date</label>
            <input required @input="updateDate()" type="date" id="inputDate" class="form-control" v-model="diary.date">
        </div>
        <div class="mb-3">
            <label for="info" class="form-label">Info</label>
            <div id="info">
                <div>Fats:</div><div>{{ diary.total_fats }} g</div>
                <div>Proteins:</div><div>{{ diary.total_proteins }} g</div>
                <div>Carbohydrates:</div><div>{{ diary.total_carbohydrates }} g</div>
                <div>Calories:</div><div>{{ diary.total_calories }} g</div>
            </div>
        </div>
        <div class="mb-3">
            <label for="inputEntries" class="form-label">Entries</label>
            <div id="inputEntries">
                <div class="row">
                    <div v-for="entry in entries" :key="entry.id" class="col-12 d-flex blue-grey lighten-3 align-items-center justify-content-end py-2 px-2">
                        <div class="me-2">
                            {{ entry.product_id.product_name }}
                        </div>
                        <div class="input-group">
                            <input @input="updateEntry(entry)" required type="number" class="form-control" v-model="entry.amount">
                            <span class="input-group-text">{{ entry.product_id.unit.unitname }}</span>
                        </div>
                        <div class="ms-2">
                            <button @click="deleteEntry(entry.id)" class="btn red darken-1 red-text text-lighten-4 py-1 px-2"><i class="bi bi-trash"></i></button>
                        </div>
                    </div>
                    <div class="mt-3 px-0 col-12">
                        <input @input="getProducts()" type="text" class="form-control mb-2" placeholder="Search for products..." v-model="searchProducts">
                        <div id="productsResult" class="blue-grey lighten-3 py-2 px-2">
                            <div v-for="product in searchedProducts" :key="product.id" class="d-flex align-items-center justify-content-end py-2">
                                <div class="flex-fill">
                                    {{ product.product_name }} ({{ product.base_amount }}{{ product.unit.unitname }})
                                </div>
                                <div>
                                    <button @click="addEntry(product)" class="btn green darken-1 green-text text-lighten-4 py-1 px-2"><i class="bi bi-plus"></i></button>
                                </div>
                            </div>
                            <div v-if="searchedProducts.length == 0">
                                Not found
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </form>
</template>

<script>
export default {
    data(){
        return {
            message: null,
            id: this.diaryData.id,
            entries: this.diaryData.entries,
            diary: {
                date: this.diaryData.date,
                total_fats: this.diaryData.total_fats,
                total_proteins: this.diaryData.total_proteins,
                total_carbohydrates: this.diaryData.total_carbohydrates,
                total_calories: this.diaryData.total_calories
            },
            searchProducts: "",
            searchedProducts: [],
        }
    },
    props: {
        diaryData: Object,
        edit: Boolean
    },
    methods: {
        async updateDate(){ // updates only the date of diary
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/diaries/' + this.id, 'PUT', {date: this.diary.date}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.refreshForm(false)
            }
        },
        async getProducts(){ // get products from search
            if (this.searchProducts.length > 0){
                const query = {
                    product_name: this.searchProducts,
                    exclude_products: (this.entries) ? this.entries.map(({product_id}) => product_id.id) : null
                }
                this.searchedProducts = await this.$fetchUtil(this.$store.getters.getUrl + '/products/filter', 'POST', query, this.$store.getters.getToken)
                if (this.searchedProducts && this.searchedProducts.detail){
                    this.searchedProducts = []
                }
            }else{
                this.searchedProducts = []
            }
        },
        async updateEntry(obj){ // updates amount in entry, also udpate diary info
            const entry = {
                amount: obj.amount
            }
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/entries/' + obj.id, 'PUT', entry, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.refreshForm(false)
            }
        },
        async deleteEntry(id){ // delete entry, also update diary info
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/entries/' + id, 'DELETE', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.refreshForm(false)
            }
        },
        async addEntry(obj){ // add new entry, also update diary info
            const entry = {
                amount: obj.base_amount,
                product_id: obj.id,
                diary_id: this.id
            }
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/entries', 'POST', entry, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.refreshForm(false)
            }
        },
        async refreshForm(close){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/diaries/' + this.id, 'GET', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                const method = (this.edit == true) ? 'PUT' : 'POST'
                this.diary.date = this.message.diary.date
                this.diary.total_fats = this.message.diary.total_fats
                this.diary.total_proteins = this.message.diary.total_proteins
                this.diary.total_carbohydrates = this.message.diary.total_carbohydrates
                this.diary.total_calories = this.message.diary.total_calories
                this.entries = this.message.entries
                this.message = null
                this.getProducts()
                this.$emit('diaryUpdate', {id: this.id, action: method, close: close})
            }
        }
    }
}
</script>

<style lang="css">
    div#info{
        display: grid;
        grid-template-columns: 50% 50%;
        align-items: center;
        grid-column-gap: 10px;
        -ms-grid-column-gap: 10px;
    }
    div#info div:nth-child(even){
        justify-self: start;
    }
    div#info div:nth-child(odd){
        justify-self: end;
    }
    .input-group{
        width: auto;
    }
</style>