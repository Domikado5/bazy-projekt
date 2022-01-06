<template>
    <form @submit.prevent="submitForm()">
        <div v-if="message && message.detail" class="red lighten-4 red-text ">
            {{ message.detail }}
        </div>
        <div class="mb-3">
            <label for="inputUnitname" class="form-label">Unitname</label>
            <input required type="text" id="inputUnitname" class="form-control" v-model="unit.unitname">
        </div>
        <div class="mb-3">
            <button class="btn orange lighten-4 orange-text" v-if="edit == true">Edit</button>
            <button class="btn blue lighten-4 blue-text" v-if="edit == false">Create</button>
        </div>
    </form>
</template>

<script>
export default {
    data(){
        return {
            message: null,
            id: this.unitData.id,
            unit: {
                unitname: this.unitData.unitname
            }
        }
    },
    props: {
        unitData: Object,
        edit: Boolean
    },
    methods: {
        async submitForm(){
            const method = (this.edit == true) ? 'PUT' : 'POST'
            const endpoint = (this.id) ? '/units/' + this.id : '/units'
            this.message = await this.$fetchUtil(this.$store.getters.getUrl + endpoint, method, this.unit, this.$store.getters.getToken)
            if (this.message && !this.message.detail){
                this.$emit('unitUpdate', {id: this.message.id, action: method})
            }
        }
    }
}
</script>