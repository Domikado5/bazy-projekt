<template>
    <form @submit.prevent="" class="mb-3 py-3 px-3 blue lighten-4">
        <div class="mb-3" v-if="message && message.detail">
            {{ message.detail }}
        </div>
        <div class="d-flex justify-content-center">
            <div v-if="type != 'Comments' && type != 'Diaries'" class="flex-fill me-3">
                <label for="inputSearch" class="form-label">{{ searchLabel }}</label>
                <input @input="sendForm()" required type="text" id="inputSearch" class="form-control" v-model="query.search" placeholder="Type something to search...">
            </div>
            <div v-if="type == 'Diaries'">
                <label for="inputDate" class="form-label">Month</label>
                <div id="inputDate" class="d-flex white">
                    <button @click="subtractMonth()" class="btn blue"><i class="bi bi-caret-left-fill"></i></button>
                    <div class="white d-flex align-items-center px-3">
                        <span :key="reload">{{ getDate() }}</span>
                    </div>
                    <button @click="addMonth()" class="btn blue"><i class="bi bi-caret-right-fill"></i></button>
                </div>
            </div>
            <div v-if="allergens" class="me-3">
                <label for="inputAllergens" class="form-label">Allergens</label>
                <select @change="sendForm()" id="inputAllergens" multiple class="form-select" v-model="query.allergens">
                    <option v-for="allergen in allergens" :key="allergen.id" :value="allergen.id">{{ allergen.allergen }}</option>
                </select>
            </div>
            <div v-if="product_categories" class="me-3">
                <label for="inputCategory" class="form-label">Category</label>
                <select @change="sendForm()" required id="inputCategory" class="form-select" v-model="query.categories" aria-label="Default select example">
                    <option :value="null">----------</option>
                    <option v-for="category in product_categories" :key="category.id" :value="category.id">{{ category.category_name }}</option>
                </select>
            </div>
            <div v-if="set_categories" class="me-3">
                <label for="inputCategory" class="form-label">Category</label>
                <select @change="sendForm()" required id="inputCategory" multiple class="form-select" v-model="query.categories" aria-label="Default select example">
                    <option v-for="category in set_categories" :key="category.id" :value="category.id">{{ category.category_name }}</option>
                </select>
            </div>
            <div v-if="type=='Products'" class="me-3">
                <label for="inputVerified" class="form-label">Verified</label>
                <select @change="sendForm()" required id="inputVerified" class="form-select" v-model="query.verified" aria-label="Default select example">
                    <option :value="null">----------</option>
                    <option value="verified">Verified</option>
                    <option value="not verified">Not Verified</option>
                </select>
            </div>
            <div v-if="type=='Users'" class="me-3">
                <label for="inputRole" class="form-label">Role</label>
                <select @change="sendForm()" required id="inputRole" class="form-select" v-model="query.role" aria-label="Default select example">
                    <option :value="null">----------</option>
                    <option value="admin">Admin</option>
                    <option value="writer">Writer</option>
                    <option value="user">User</option>
                </select>
            </div>
            <div v-if="sorts">
                <label for="inputSort1" class="form-label">Sort</label>
                <select @change="sendForm()" required id="inputSort1" class="form-select" v-model="query.sort" aria-label="Default select example">
                    <option v-for="sort in sorts" :key="sort.id" :value="sort.id">{{ sort.text }}</option>
                </select>
            </div>
        </div>

    </form>
</template>

<script>
export default {
    data(){
        return {
            message: null,
            date: this.dateData,
            reload: 0,
            query: {
                search: null,
                sort: null,
                allergens: null,
                categories: null,
                verified: null,
                role: null
            },
            sorts: null,
            allergens: this.allergensData,
            product_categories: this.productCategoriesData,
            set_categories: this.setCategoriesData,
            search: null,
            searchLabel: null
        }
    },
    props: {
        type: String,
        allergensData: Array,
        productCategoriesData: Array,
        setCategoriesData: Array,
        dateData: Date
    },
    methods: {
        async sendForm(){
            this.$emit('search-update', this.query)
        },
        addMonth(){
            const d = this.date.getDate()
            this.date.setMonth(this.date.getMonth() + 1)
            if (this.date.getDate() != d) {
               this.date.setDate(0);
            }
            this.reload++
            this.$emit('searchUpdate', {date: this.date})
        },
        subtractMonth(){
            const d = this.date.getDate()
            this.date.setMonth(this.date.getMonth() - 1)
            if (this.date.getDate() != d) {
               this.date.setDate(0);
            }
            this.reload++
            this.$emit('searchUpdate', {date: this.date})
        },
        getDate(){
            return `${this.date.getFullYear()} - ${this.date.getMonth() + 1}`
        }
    },
    created(){
        if (this.type == "Posts"){
            this.sorts = [{id: 'title', text: 'Title Ascending'}, {id: '-title', text: 'Title Descending'}, {id: 'date', text: 'Date Ascending'}, {id: '-date', text: 'Date Descending'}]
            this.query.sort = this.sorts[0].id
            this.searchLabel = 'Post Title'
        }else if (this.type == "Products"){
            this.sorts = [
                {id: 'product_name', text: 'Product Name Ascending'},
                {id: '-product_name', text: 'Product Name Descending'},
                {id: 'fats', text: 'Fats Ascending'},
                {id: '-fats', text: 'Fats Descending'},
                {id: 'proteins', text: 'Proteins Ascending'},
                {id: '-proteins', text: 'Proteins Descending'},
                {id: 'carbohydrates', text: 'Carbohydrates Ascending'},
                {id: '-carbohydrates', text: 'Carbohydrates Descending'},
                {id: 'calories', text: 'Calories Ascending'},
                {id: '-calories', text: 'Calories Descending'},
            ]
            this.query.sort = this.sorts[0].id
            this.query.allergens = []
            this.searchLabel = 'Product Name'
        }else if (this.type == "Comments"){
            this.sorts = [
                {id: '-date', text: 'Newest'},
                {id: 'date', text: 'Oldest'}
            ]
            this.query.sort = this.sorts[0].id
        }else if (this.type == "Diaries"){
            console.log("Diaries :-)")
        }else if (this.type == "Users"){
            this.sorts = [
                {id: 'id', text: 'ID Ascending'},
                {id: '-id', text: 'ID Ascending'},
                {id: 'username', text: 'Username Ascending'},
                {id: '-username', text: 'Username Descending'}
            ]
            this.query.sort = this.sorts[0].id
            this.searchLabel = 'Username'
        }else if (this.type == 'Sets'){
            this.sorts = [
                {id: 'set_name', text: 'Set Name Ascending'},
                {id: '-set_name', text: 'Set Name Descending'}
            ]
            this.query.sort = this.sorts[0].id
            this.query.categories = []
            this.searchLabel = 'Set Name'
        }
    }
}
</script>