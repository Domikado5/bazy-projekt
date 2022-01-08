<template>
    <div class="container-fluid">
        <h1>Products List - Page {{ $route.params.page }}</h1>
        <div class="red lighten-4 red-text" v-if="message && message.detail">{{ message.detail }}</div>
        <div class="row" v-if="allergens && categories">
            <search-form @search-update="updateQuery($event)" type="Products" :allergens-data="allergens" :product-categories-data="categories"></search-form>
        </div>
        <div class="table-responsive">
        <div v-if="products && products.length == 0">
            <h2>Not found</h2>
        </div>
        <table class="table table-striped" v-if="products && products.length > 0">
            <thead>
                <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Product Name</th>
                    <th scope="col">Category</th>
                    <th scope="col">Fats</th>
                    <th scope="col">Proteins</th>
                    <th scope="col">Carbs</th>
                    <th scope="col">Calories</th>
                    <th scope="col">Base Amount</th>
                    <th scope="col">Unit</th>
                    <th scope="col">Verified</th>
                    <th scope="col">Allergens</th>
                    <th scope="col" v-if="$store.getters.getUser && $store.getters.getUser.role == 'admin'">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="product in products" :key="product.id">
                    <th>{{ product.id }}</th>
                    <td>{{ product.product_name }}</td>
                    <td>{{ product.categories.category_name }}</td>
                    <td>{{ product.fats }}</td>
                    <td>{{ product.proteins }}</td>
                    <td>{{ product.carbohydrates }}</td>
                    <td>{{ product.calories }}</td>
                    <td>{{ product.base_amount }}</td>
                    <td>{{ product.unit.unitname }}</td>
                    <td>{{ product.verified }}</td>
                    <td>{{ product.allergens.length }}</td>
                    <td v-if="$store.getters.getUser && $store.getters.getUser.role == 'admin'">
                        <button class="btn orange lighten-4 orange-text" data-bs-toggle="modal" :data-bs-target="'#editModal' + product.id">Edit</button>
                        <button class="btn red lighten-4 red-text ms-2" data-bs-toggle="modal" :data-bs-target="'#deleteModal' + product.id">Delete</button>
                    </td>
                    <div class="modal fade" :id="'deleteModal' + product.id" tabindex="-1" :aria-labelledby="'deleteModalLabel' + product.id" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-scrollable">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" :id="'deleteModalLabel' + product.id">Are you sure?</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <h6>You are deleting <span class="blue-text">{{ product.product_name }}</span></h6>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" @click="deleteProduct(product.id)" class="btn red lighten-4 red-text">Yes</button>
                                    <button type="button" class="btn green lighten-4 green-text" data-bs-dismiss="modal">No</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal fade" :id="'editModal' + product.id" tabindex="-1" :aria-labelledby="'editModalLabel' + product.id" aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" :id="'editModalLabel' + product.id">Edit Product</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <product-form @product-update="refreshList($event)" :product-data="product" :categories-data="categories" :units-data="units" :allergens-data="allergens" :edit="true"></product-form>
                            </div>
                            </div>
                        </div>
                    </div>
                </tr>
            </tbody>
        </table>
        </div>
    </div>
</template>

<script>
import ProductForm from '@/components/ProductForm.vue'
import SearchForm from '@/components/SearchForm.vue'
export default {
    components: { ProductForm, SearchForm },
    data(){
        return {
            products: null,
            message: null,
            query: {
                product_name: null,
                categories: null, 
                allergens: null,
                verified: null,
                sort: null,
            },
            categories: null,
            units: null,
            allergens: null,
        }
    },
    methods: {
        async getSelects(){
            this.categories = await this.$fetchUtil(this.$store.getters.getUrl + '/product_categories', 'GET', {}, this.$store.getters.getToken)
            this.units = await this.$fetchUtil(this.$store.getters.getUrl + '/units', 'GET', {}, this.$store.getters.getToken)
            this.allergens = await this.$fetchUtil(this.$store.getters.getUrl + '/allergens', 'GET', {}, this.$store.getters.getToken)
        },
        async getProducts(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/products/page/' + this.$route.params.page, 'POST', this.query, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.products = this.message
                this.message = null
            }
        },
        async deleteProduct(id){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/products/' + id, 'DELETE', {}, this.$store.getters.getToken)
            document.querySelector("#deleteModalLabel" + id + " + button").click()
            if (this.message && !this.message.detail){
                this.getProducts()
            }
        },
        refreshList(id){
            document.querySelector('#editModalLabel' + id + ' + button').click()
            this.getProducts()
        },
        updateQuery(q){
            this.query = {
                product_name: q.search,
                categories: q.categories, 
                allergens: (q.allergens) ? q.allergens : [],
                verified: q.verified,
                sort: q.sort,
            }
            console.log(q)
            this.getProducts()
        }
    },
    created(){
        this.getSelects()
        this.getProducts()
    }
}
</script>