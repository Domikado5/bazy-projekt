<template>
    <div class="container-fluid">
        <div class="red lighten-4 red" v-if="message && message.detail">{{ message.detail }}</div>
        <div class="row" v-if="product">
            <h2>{{ product.product_name }} <span class="badge white-text" :class="{'green': product.verified == 'verified', 'red': product.verified != 'verified'}">{{ product.verified }}</span></h2>
            <h3 class="purple-text text-accent-2">{{ product.categories.category_name }}</h3>
            <h3>Fats: {{ product.fats }}g</h3>
            <h3>Proteins: {{ product.proteins }}g</h3>
            <h3>Carbohydrates: {{ product.carbohydrates }}g</h3>
            <h3>Calories: {{ product.calories }}kcal</h3>
            <h3>Amount: {{ product.base_amount }} {{ product.unit.unitname }}</h3>
            <h3 v-if="product.allergens.length > 0">Allergens:</h3>
            <h4 v-for="allergen in product.allergens" :key="allergen.id">{{ allergen.allergen }}</h4>
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return {
            message: null,
            product: null
        }
    },
    methods: {
        async getProduct(id){
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + '/products/' + id, 'GET', {}, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.product = this.message
                this.message = null
            }
        }
    },
    created(){
        this.getProduct(this.$route.params.id)
    }
}
</script>