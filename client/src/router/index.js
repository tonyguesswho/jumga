import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
// import store from '../store';
import Register from '../views/Register'
import Login from '../views/Login'
import Seller from '../views/Seller'
import Dashboard from '../views/Dashboard'
import Verify from '../views/Verify'
import AddProduct from '../views/AddProduct'
import AddAccount from '../views/AddAccount'

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/register',
    name: "Register",
    component: Register,
    meta: { guest: true },
  },
  {
    path: '/login',
    name: "Login",
    component: Login,
    meta: { guest: true },
  },
  {
    path: '/seller',
    name: Seller,
    component: Seller,
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard',
    name: Dashboard,
    component: Dashboard,
    meta: { requiresAuth: true },
  },
  {
    path: '/sellerpayment',
    name: Verify,
    component: Verify,
    meta: { requiresAuth: true },
  },
  {
    path: '/addproduct',
    name: AddProduct,
    component: AddProduct,
    meta: { requiresAuth: true },
  },
  {
    path: '/addaccount',
    name: AddAccount,
    component: AddAccount,
    meta: { requiresAuth: true },
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

// router.beforeEach((to, from, next) => {
//   if(to.matched.some(record => record.meta.requiresAuth)) {
//     if (store.getters.isAuthenticated) {
//       next()
//       return
//     }
//     next('/login')
//   } else {
//     next()
//   }
// })
// router.beforeEach((to, from, next) => {
//   if (to.matched.some((record) => record.meta.guest)) {
//     if (store.getters.isAuthenticated) {
//       next("/seller");
//       return;
//     }
//     next();
//   } else {
//     next();
//   }
// });

export default router;
