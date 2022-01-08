<template>
    <div class="container-fluid">
        <h1>Add New Product</h1>
        <div v-if="categories && allergens && units">
            <product-form @product-update="showProduct($event)" :product-data="product" :edit="false" :categories-data="categories" :units-data="units" :allergens-data="allergens"></product-form>
        </div>
    </div>
</template>

<script>
import ProductForm from '@/components/ProductForm.vue'
export default {
  components: { ProductForm },
    data(){
        return {
            product: {
                id: null,
                product_name: "",
                categories: null,
                fats: 0,
                proteins: 0,
                carbohydrates: 0,
                calories: 0,
                base_amount: 0,
                unit: null,
                verified: 'verified',
                allergens: []
            },
            categories: null,
            units: null,
            allergens: null
        }
    },
    methods: {
        showProduct(id){
            this.$router.push("/product/" + id)
        },
        async getSelects(){
            this.categories = await this.$fetchUtil(this.$store.getters.getUrl + '/product_categories', 'GET', {}, this.$store.getters.getToken)
            this.units = await this.$fetchUtil(this.$store.getters.getUrl + '/units', 'GET', {}, this.$store.getters.getToken)
            this.allergens = await this.$fetchUtil(this.$store.getters.getUrl + '/allergens', 'GET', {}, this.$store.getters.getToken)
        }
    },
    created(){
        this.getSelects()
    }
}
</script>