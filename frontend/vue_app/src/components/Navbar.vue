<template>
  <nav class="navbar navbar-expand-lg navbar-dark light-blue darken-4">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">Fitapka</router-link>
      <button
        class="navbar-toggler"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" active-class="active" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" active-class="active" to="/blog">Blog</router-link>
          </li>
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              id="navbarDropdown"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <span :class="{'white-text': ['Products - List', 'Products - Add'].includes($route.name)}">Products</span>
            </a>
            <ul
              class="dropdown-menu dropdown-menu-dark dropdown-menu-start"
              aria-labelledby="navbarDropdown"
            >
              <li><router-link to="/products/1" class="dropdown-item">List Products</router-link></li>
              <li><hr class="dropdown-divider" /></li>
              <li><router-link to="/add_product" class="dropdown-item">Add New Product</router-link></li>
            </ul>
          </li>
          <li class="nav-item" v-if="$store.getters.getUser && $store.getters.getUser.role == 'admin'">
            <router-link class="nav-link" active-class="active" to="/users/1">Users</router-link>
          </li>
        </ul>
        <li class="dropdown" v-if="$store.getters.getToken != null">
            <button class="btn btn-outline-dark dropdown-toggle" type="button" data-bs-display="static" id="userDropdown" data-bs-toggle="dropdown" aria-expanded="false">
              {{ $store.getters.getUser.username }}
            </button>
            <ul
              class="dropdown-menu dropdown-menu-dark dropdown-menu-lg-end "
              aria-labelledby="userDropdown"
            >
              <li><router-link :to="'/account/' + $store.getters.getUser.id" class="dropdown-item">Your Profile</router-link></li>
              <li><a href="#" class="dropdown-item">Your Diaries</a></li>
              <li><hr class="dropdown-divider" /></li>
              <li><a href="#" @click="logout" class="dropdown-item">Logout</a></li>
            </ul>
        </li>
        <router-link v-else class="btn btn-outline-dark" active-class="active" to="/login">Login</router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  methods: {
    logout(){
      this.$store.commit('resetToken')
      this.$router.push({path: "/"})
    }
  }
};
</script>

<style lang="scss" scoped>
.nav-item{
  display: grid;
  place-items: center;
}
</style>
