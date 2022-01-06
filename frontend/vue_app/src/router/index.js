import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Login from "@/views/Login.vue";
import Register from "@/views/Users/Register.vue"
import Account from "@/views/Users/Account.vue"
import UsersList from "@/views/Users/UsersList.vue"
import Blog from "@/views/Posts/Blog.vue";
import Post from "@/views/Posts/Post.vue";
import PostCreate from "@/views/Posts/PostCreate.vue";
import PostEdit from "@/views/Posts/PostEdit.vue";
import ProductsList from "@/views/Products/ProductsList.vue";
import AddProduct from "@/views/Products/AddProduct.vue"
import Product from "@/views/Products/Product.vue"
import ProductCategories from "@/views/Products/Categories.vue"
import Allergens from "@/views/Products/Allergens.vue"

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/blog",
    name: "Blog",
    component: Blog,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/account/:id",
    name: "User - account",
    component: Account,
  },
  {
    path: "/users/:page",
    name: "Users - List",
    component: UsersList,
  },
  {
    path: "/post/:id",
    name: "Post",
    component: Post
  },
  {
    path: "/post/create",
    name: "Post - Create",
    component: PostCreate
  },
  {
    path: "/post/edit/:id",
    name: "Post - Edit",
    component: PostEdit
  },
  {
    path: "/products/:page",
    name: "Products - List",
    component: ProductsList
  },
  {
    path: "/add_product",
    name: "Products - Add",
    component: AddProduct
  },
  {
    path: "/product/:id",
    name: "Product",
    component: Product
  },
  {
    path: "/product_categories/:page",
    name: "Products - Categories",
    component: ProductCategories
  },
  {
    path: "/allergens/:page",
    name: "Products - Allergens",
    component: Allergens
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
