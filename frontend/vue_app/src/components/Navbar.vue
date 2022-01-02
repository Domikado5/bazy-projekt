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
              Products
            </a>
            <ul
              class="dropdown-menu dropdown-menu-dark dropdown-menu-start"
              aria-labelledby="navbarDropdown"
            >
              <li><a href="#" class="dropdown-item">List Products</a></li>
              <li><hr class="dropdown-divider" /></li>
              <li><a href="#" class="dropdown-item">Add New Product</a></li>
            </ul>
          </li>
        </ul>
        <li class="dropdown" v-if="$store.getters.getToken != null">
            <button class="btn btn-outline-dark dropdown-toggle" type="button" data-bs-display="static" id="userDropdown" data-bs-toggle="dropdown" aria-expanded="false">
              User
            </button>
            <ul
              class="dropdown-menu dropdown-menu-dark dropdown-menu-lg-end "
              aria-labelledby="userDropdown"
            >
              <li><a href="#" class="dropdown-item">Your Profile</a></li>
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
