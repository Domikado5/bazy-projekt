<template>
    <form @submit.prevent="submitForm()">
        <div v-if="message && message.detail" class="red lighten-4 red-text ">
            {{ message.detail }}
        </div>
        <div class="mb-3">
            <label for="inputAllergen" class="form-label">Allergen</label>
            <input required type="text" id="inputAllergen" class="form-control" v-model="allergen.allergen">
        </div>
        <div class="mb-3">
            <button class="btn orange lighten-4 orange-text" v-if="edit == true">Edit Allergen</button>
            <button class="btn blue lighten-4 blue-text" v-if="edit == false">Create Allergen</button>
        </div>
    </form>
</template>

<script>
export default {
    data(){
        return {
            message: null,
            id: this.allergenData.id,
            allergen: {
                allergen: this.allergenData.allergen
            }
        }
    },
    props: {
        allergenData: Object,
        edit: Boolean
    },
    methods: {
        async submitForm(){
            const method = (this.edit == true) ? 'PUT' : 'POST'
            const endpoint = (this.id) ? '/allergens/' + this.id : '/allergens'
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + endpoint, method, this.allergen, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.$emit('allergenUpdate', {id: this.message.id, action: method})
            }
        }
    }
}
</script>