<template>
    <form @submit.prevent="">
        <div v-if="message && message.detail" class="red lighten-4 red-text ">
            {{ message.detail }}
        </div>
        <div class="mb-3">
            <label for="inputSetName" class="form-label">Set Name</label>
            <input required type="text" id="inputSetName" class="form-control" v-model="set.set_name">
        </div>
        <div class="mb-3">
            <label for="inputDescription" class="form-label">Description</label>
            <textarea required id="inputDescription" class="form-control" v-model="set.description"></textarea>
        </div>
        <div class="mb-3">
            <label for="inputProducts" class="form-label">Products</label>
            <div id="inputProducts">
                <div class="row">
                    <div v-for="product in set.products" :key="product.id" class="col-12 d-flex blue-grey lighten-3 align-items-center justify-content-end py-2 px-2">
                        <div class="flex-fill">
                            {{ product.product_name }}
                        </div>
                        <div>
                            <button @click="removeProduct(product)" class="btn red darken-1 red-text text-lighten-4 py-1 px-2"><i class="bi bi-trash"></i></button>
                        </div>
                    </div>
                    <div class="mt-3 px-0 col-12">
                        <input @input="getProducts()" type="text" class="form-control mb-2" placeholder="Search for products..." v-model="searchProducts">
                        <div id="productsResult" class="blue-grey lighten-3 py-2 px-2">
                            <div v-for="product in searchedProducts" :key="product.id" class="d-flex align-items-center justify-content-end py-2">
                                <div class="flex-fill">
                                    {{ product.product_name }}
                                </div>
                                <div>
                                    <button @click="addProduct(product)" class="btn green darken-1 green-text text-lighten-4 py-1 px-2"><i class="bi bi-plus"></i></button>
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
        <div class="mb-3 my-3">
            <label for="inputCategories" class="form-label">Categories</label>
            <select id="inputCategories" multiple class="form-select" v-model="set.categories">
                <option v-for="category in categories" :selected="set.categories.includes(category.id)" :key="category.id" :value="category.id">{{ category.category_name }}</option>
            </select>
        </div>
        <div class="mb-3">
            <button @click="submitForm()" v-if="edit == true" class="btn orange lighten-4 orange-text">Edit</button>
            <button @click="submitForm()" v-if="edit == false" class="btn blue lighten-4 blue-text">Create</button>
        </div>
    </form>
</template>

<script>
export default {
    data(){
        return {
            message: null,
            id: this.setData.id,
            set: {
                set_name: this.setData.set_name,
                description: this.setData.description,
                products: this.setData.products,
                categories: (this.setData.categories && this.setData.categories.length > 0) ? this.setData.categories.map(({id}) => id) : [],
                owner: 0
            },
            searchProducts: "",
            searchedProducts: [],
            categories: this.categoriesData
        }
    },
    props: {
        setData: Object,
        categoriesData: Array,
        edit: Boolean
    },
    methods: {
        async getProducts(){
            if (this.searchProducts.length > 0){
                const query = {
                    product_name: this.searchProducts,
                    exclude_products: (this.set.products) ? this.set.products.map(({id}) => id) : null
                }
                this.searchedProducts = await this.$fetchUtil(this.$store.getters.getUrl + '/products/filter', 'POST', query, this.$store.getters.getToken)
                if (this.searchedProducts && this.searchedProducts.detail){
                    this.searchedProducts = []
                }
            }else{
                this.searchedProducts = []
            }
        },
        addProduct(item){
            this.set.products.push(item)
            this.getProducts()
        },
        removeProduct(item){
            this.set.products = this.set.products.filter((product) => product.id != item.id)
            this.getProducts()
        },
        async submitForm(){
            const method = (this.edit == true) ? 'PUT' : 'POST'
            const endpoint = (this.id) ? '/sets/' + this.id : '/sets'
            let set = this.set
            set.products = set.products.map(({id}) => id)
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + endpoint, method, set, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.$emit('setUpdate', {id: this.message.id, action: method})
            }
        }
    }
}
</script>