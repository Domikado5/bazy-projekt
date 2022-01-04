<template>
    <div class="container-fluid">
        <h1>Products List - Page {{ $route.params.page }}</h1>
        <div class="red lighten-4 red-text" v-if="message && message.detail">{{ message.detail }}</div>
        <table class="table table-striped">
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
                    <th scope="col">Verified</th>
                    <th scope="col">Allergens</th>
                    <th scope="col">Unit</th>
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
                    <td>{{ product.verified }}</td>
                    <td>{{ product.allergens.length }}</td>
                    <td>{{ product.unit.unitname }}</td>
                    <td v-if="$store.getters.getUser && $store.getters.getUser.role == 'admin'">
                        <button class="btn orange lighten-4 orange-text">Edit</button>
                        <button class="btn red lighten-4 red-text ms-2">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    data(){
        return {
            products: null,
            message: null,
        }
    },
    methods: {
        async getProducts(){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/products/page/' + this.$route.params.page, 'GET', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.products = this.message
                console.log(this.products)
                this.message = null
            }
        }
    },
    created(){
        this.getProducts()
    }
}
</script>