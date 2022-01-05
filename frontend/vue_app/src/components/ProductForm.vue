<template>
    <form @submit.prevent="resolveProduct()" class="row">
        <div v-if="message && message.detail" class="red lighten-4 red-text ">
            {{ message.detail }}
        </div>
        <div class="mb-3 col-12">
            <label for="inputProductName" class="form-label">Product Name</label>
            <input required type="text" id="inputProductName" class="form-control" v-model="product.product_name">
        </div>
        <div class="mb-3 col-12">
            <label for="inputCategory" class="form-label">Category</label>
            <select required id="inputCategory" class="form-select" v-model="product.categories" aria-label="Default select example">
                <option v-for="category in categories" :key="category.id" :selected="product.categories == category.id" :value="category.id">{{ category.category_name }}</option>
            </select>
        </div>
        <div class="mb-3 col-12 col-lg-6">
            <label for="inputFats" class="form-label">Fats</label>
            <input type="number" id="inputFats" class="form-control" v-model="product.fats">
        </div>
        <div class="mb-3 col-12 col-lg-6">
            <label for="inputProteins" class="form-label">Proteins</label>
            <input type="number" id="inputProteins" class="form-control" v-model="product.proteins">
        </div>
        <div class="mb-3 col-12 col-lg-6">
            <label for="inputCarbohydrates" class="form-label">Carbohydrates</label>
            <input type="number" id="inputCarbohydrates" class="form-control" v-model="product.carbohydrates">
        </div>
        <div class="mb-3 col-12 col-lg-6">
            <label for="inputCalories" class="form-label">Calories</label>
            <input type="number" id="inputCalories" class="form-control" v-model="product.calories">
        </div>
        <div class="mb-3 col-12 col-lg-6">
            <label for="inputBaseAmount" class="form-label">Base Amount</label>
            <input type="number" id="inputBaseAmount" class="form-control" v-model="product.base_amount">
        </div>
        <div class="mb-3 col-12 col-lg-6">
            <label for="inputUnit" class="form-label">Unit</label>
            <select required id="inputUnit" class="form-select" v-model="product.unit">
                <option v-for="unit in units" :key="unit.id" :selected="product.unit == unit.id" :value="unit.id">{{ unit.unitname }}</option>
            </select>
        </div>
        <div class="mb-3 col-12">
            <label for="inputAllergens" class="form-label">Allergens</label>
            <select id="inputAllergens" multiple class="form-select" v-model="product.allergens">
                <option v-for="allergen in allergens" :selected="product.allergens.includes(allergen.id)" :key="allergen.id" :value="allergen.id">{{ allergen.allergen }}</option>
            </select>
        </div>
        <div class="mb-3 col-12" v-if="$store.getters.getUser && $store.getters.getUser.role != 'user'">
            <input type="checkbox" id="inputVerified" class="form-check-input" v-model="verified" :checked="product.verified == 'verified'">
            <label for="inputVerified" class="form-check-label">Verified</label>
        </div>
        <div class="col-12">
            <button v-if="edit == true" class="btn orange lighten-4 orange-text">Edit Product</button>
            <button v-else class="btn blue lighten-4 blue-text">Add Product</button>
        </div>
    </form>
</template>

<script>
export default {
    data(){
        return {
            message: null,
            categories: null,
            units: null,
            allergens: null,
            verified: this.productData.verified == 'verified',
            prod_id: this.productData.id,
            product: {
                product_name: this.productData.product_name,
                categories: (this.productData.categories) ? this.productData.categories.id : null, // contains only ID
                fats: this.productData.fats,
                proteins: this.productData.proteins,
                carbohydrates: this.productData.carbohydrates,
                calories: this.productData.calories,
                base_amount: this.productData.base_amount,
                unit: (this.productData.unit) ? this.productData.unit.id : null, // contains only ID
                verified: this.productData.verified,
                allergens: (this.productData.allergens.length > 0) ? this.productData.allergens.map(({ id }) => id) : [] // contains only array of ID or empty array
            }
        }
    },
    props: {
        productData: Object,
        edit: Boolean
    },
    methods: {
        async getSelects(){
            this.categories = await this.$fetchUtil(this.$store.getters.getUrl + '/product_categories', 'GET', {}, this.$store.getters.getToken)
            this.units = await this.$fetchUtil(this.$store.getters.getUrl + '/units', 'GET', {}, this.$store.getters.getToken)
            this.allergens = await this.$fetchUtil(this.$store.getters.getUrl + '/allergens', 'GET', {}, this.$store.getters.getToken)
        },
        async resolveProduct(){
            const method = (this.edit == true) ? 'PUT' : 'POST'
            const endpoint = (this.prod_id) ? '/products/' + this.prod_id : '/products'
            this.product.verified = (this.verified) ? 'verified' : 'not verified'
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + endpoint, method, this.product, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.$emit('productUpdate', this.message.id)
            }
        }
    },
    created(){
        this.getSelects()
    }
}
</script>