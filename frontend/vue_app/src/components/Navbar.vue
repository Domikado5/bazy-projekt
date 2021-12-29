<template>
  <nav class="navbar navbar-expand-lg navbar-dark light-blue darken-4">
    <div class="container-fluid">
      <a href="#" class="navbar-brand">Fitapka</a>
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
              class="dropdown-menu dropdown-menu-dark"
              aria-labelledby="navbarDropdown"
            >
              <li><a href="#" class="dropdown-item">List Products</a></li>
              <li><hr class="dropdown-divider" /></li>
              <li><a href="#" class="dropdown-item">Add New Product</a></li>
            </ul>
          </li>
        </ul>
        <router-link class="btn btn-outline-dark" active-class="active" to="/login">Login</router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  setup() {},
};
</script>

<style lang="scss" scoped>
.nav-item{
  display: grid;
  place-items: center;
}
</style>
