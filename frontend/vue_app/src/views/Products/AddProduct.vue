<template>
    <div class="container-fluid">
        <h1>Add New Product</h1>
        <product-form @product-update="showProduct($event)" :product-data="product" edit="false"></product-form>
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
            }
        }
    },
    methods: {
        showProduct(id){
            this.$router.push("/product/" + id)
        }
    },
    created(){

    }
}
</script>