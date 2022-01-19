<template>
    <nav aria-label="Page navigation example" class="mt-3 d-flex justify-content-center" v-if="max && max > 0">
        <ul class="pagination">
            <li class="page-item" :class="{'disabled': page == 1}">
                <a href="#" class="page-link" aria-label="Previous" @click="prevPage()">
                    <span aria-hidden="true">&laquo;</span>
                </a>
            </li>
            <li class="page-item" v-for="idx in maxPage" :key="idx" :class="{'active': idx == page}">
                <a href="#" class="page-link" @click="changePage(idx)">{{ idx }}</a>
            </li>
            <li class="page-item" :class="{'disabled': page == maxPage}">
                <a href="#" class="page-link" aria-label="Next" @click="nextPage()">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            </li>
        </ul>
    </nav>
</template>

<script>
export default {
    data(){
        return {
            page: 1,
            maxPage: this.max,
        }
    },
    methods: {
        changePage(page){
            this.page = page
            this.updatePage()
        },
        nextPage(){
            this.page++
            this.updatePage()
        },
        prevPage(){
            this.page--
            this.updatePage()
        },
        updatePage(){
            this.$emit('pageUpdate', this.page)
        }
    },
    props: {
        max: Number
    }
}
</script>