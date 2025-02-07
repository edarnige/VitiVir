import Vue from "vue";
import Router from "vue-router";
//import Index from "./views/Index.vue";
import Landing from "./views/Landing.vue";
import Login from "./views/Login.vue";
import Signup from "./views/Signup";
import Search from "./views/Search.vue";
import EntryDetail from "./views/EntryDetail.vue";
import Blast from "./views/Blast.vue";
import MainNavbar from "./layout/MainNavbar.vue";
import MainFooter from "./layout/MainFooter.vue";


Vue.use(Router);

export default new Router({
  routes: [
    // {
    //   path: "/",
    //   name: "index",
    //   components: { default: Index, header: MainNavbar, footer: MainFooter },
    //   props: {
    //     header: { colorOnScroll: 400 },
    //     footer: { backgroundColor: "black" }
    //   }
    // },
    {
      path: "/",
      name: "landing",
      components: { default: Landing, header: MainNavbar, footer: MainFooter },
      props: {
        footer: { backgroundColor: "black" }
      }
    },
    {
      path: "/login",
      name: "login",
      components: { default: Login, header: MainNavbar, footer: MainFooter },
      props: {

      }
    },
    {
      path: "/signup",
      name: "signup",
      components: { default: Signup, header: MainNavbar, footer: MainFooter },
      props: {

      }
    },
    {
      path: "/search",
      name: "search",
      components: { default: Search, header: MainNavbar, footer: MainFooter },
      props: {

      },
      meta: {
        progress: {
          func: [
            {call: 'color', modifier: 'temp', argument: '#ffb000'},
            {call: 'fail', modifier: 'temp', argument: '#6e0000'},
            {call: 'location', modifier: 'temp', argument: 'top'},
            {call: 'transition', modifier: 'temp', argument: {speed: '1.5s', opacity: '0.6s', termination: 400}}
          ]
        }
      }
      
    },
    {
      path: "/search/:entry_id", 
      name: "entrydetail",
      components: { default: EntryDetail, header: MainNavbar, footer: MainFooter }, 
      props: { //props: true,

      }
    },
    {
      path: "/blast",
      name: "blast",
      components: { default: Blast, header: MainNavbar, footer: MainFooter },
      props: {
        footer: { backgroundColor: "black" }
      }
    },
  ],
  scrollBehavior: to => {
    if (to.hash) {
      return { selector: to.hash };
    } else {
      return { x: 0, y: 0 };
    }
  }
});
