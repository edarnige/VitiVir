<template >
  <md-toolbar
    id="toolbar"
    md-elevation="0"
    class="md-primary md-absolute"
    :class="extraNavClasses"
    :color-on-scroll="colorOnScroll"
    
  >
    <div class="md-toolbar-row md-collapse-lateral" >
      <div class="md-toolbar-section-start" >
        <h3 class="md-title">VitiVir</h3>
      </div>
      <div class="md-toolbar-section-end">
        <md-button
          class="md-just-icon md-simple md-toolbar-toggle"
          :class="{ toggled: toggledClass }"
          @click="toggleNavbarMobile()"
        >
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </md-button>

        <div class="md-collapse">
          <div class="md-collapse-wrapper">
            <mobile-menu nav-mobile-section-start="false" >
              <!-- Here you can add your items from the section-start of your toolbar -->
            </mobile-menu>
            <md-list>
            
              <li class="md-list-item" v-if="!showDownload">
                <a
                  href="javascript:void(0)"
                  class="md-list-item-router md-list-item-container md-button-clean dropdown"
                >
                  <div class="md-list-item-content">
                      <md-button
                        slot="title"
                        class="md-button md-button-link md-white md-simple "
                        @click="$router.push('/');"
                      >
                        <p>Home</p>
                      </md-button>
                  </div>
                </a>
              </li>

              <li class="md-list-item" v-if="!showDownload && this.$store.state.token==null">
                <a
                  href="javascript:void(0)"
                  class="md-list-item-router md-list-item-container md-button-clean dropdown"
                >
                  <div class="md-list-item-content" >
                      <md-button
                        slot="title"
                        class="md-button md-button-link md-white md-simple "
                        @click="$router.push('/login');"
                      >
                        <p>Login</p>
                      </md-button>
                  </div>
                </a>
              </li>

              <li class="md-list-item" v-if="!showDownload && this.$store.state.token==null">
                <a
                  href="javascript:void(0)"
                  class="md-list-item-router md-list-item-container md-button-clean dropdown"
                >
                  <div class="md-list-item-content">
                      <md-button
                        slot="title"
                        class="md-button md-button-link md-white md-simple "
                        @click="$router.push('/signup');"
                      >
                        <p>Request account</p>
                      </md-button>
                  </div>
                </a>
              </li>
              <li class="md-list-item" v-if="!showDownload && this.$store.state.token!=null" >
                <a
                  href="javascript:void(0)"
                  class="md-list-item-router md-list-item-container md-button-clean dropdown"
                >
                  <div class="md-list-item-content">
                      <md-button
                        slot="title"
                        class="md-button md-button-link md-white md-simple "
                        @click="$router.push('/search');"
                      >
                        <p>SEARCH</p>
                      </md-button>
                  </div>
                </a>
              </li>
              <li class="md-list-item" v-if="!showDownload && this.$store.state.token!=null" >
                <a
                  href="javascript:void(0)"
                  class="md-list-item-router md-list-item-container md-button-clean dropdown"
                >
                  <div class="md-list-item-content">
                      <md-button
                        slot="title"
                        class="md-button md-button-link md-white md-simple "
                        @click="$router.push('/blast');"
                      >
                        <p>BLAST</p>
                      </md-button>
                  </div>
                </a>
              </li>
              <li class="md-list-item" v-if="!showDownload && this.$store.state.token!=null" >
                <a
                  href="javascript:void(0)"
                  class="md-list-item-router md-list-item-container md-button-clean dropdown"
                >
                  <div class="md-list-item-content">
                      <md-button
                        slot="title"
                        class="md-button md-button-link md-white md-simple "
                        @click="logout()"
                      >
                        <p>Logout</p>
                      </md-button>
                  </div>
                </a>
              </li>

            </md-list>
          
          </div>
        </div>
      </div>
    </div>
  </md-toolbar>
</template>

<script>
let resizeTimeout;
function resizeThrottler(actualResizeHandler) {
  // ignore resize events as long as an actualResizeHandler execution is in the queue
  if (!resizeTimeout) {
    resizeTimeout = setTimeout(() => {
      resizeTimeout = null;
      actualResizeHandler();

      // The actualResizeHandler will execute at a rate of 15fps
    }, 66);
  }
}


import MobileMenu from "@/layout/MobileMenu";

export default {
  components: {
    MobileMenu
  },
  props: {
    type: {
      type: String,
      default: "white",
      validator(value) {
        return [
          "white",
          "default",
          "primary",
          "danger",
          "success",
          "warning",
          "info"
        ].includes(value);
      }
    },
    colorOnScroll: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      extraNavClasses: "",
      toggledClass: false,
    };
  },
  computed: {
    showDownload() {
      const excludedRoutes = ["login", "landing", "search", "signup","entrydetail", "blast"];
      return excludedRoutes.every(r => r !== this.$route.name);
    }
  },
  methods: {
    bodyClick() {
      let bodyClick = document.getElementById("bodyClick");

      if (bodyClick === null) {
        let body = document.querySelector("body");
        let elem = document.createElement("div");
        elem.setAttribute("id", "bodyClick");
        body.appendChild(elem);

        let bodyClick = document.getElementById("bodyClick");
        bodyClick.addEventListener("click", this.toggleNavbarMobile);
      } else {
        bodyClick.remove();
      }
    },
    toggleNavbarMobile() {
      this.NavbarStore.showNavbar = !this.NavbarStore.showNavbar;
      this.toggledClass = !this.toggledClass;
      this.bodyClick();
    },
    handleScroll() {
      let scrollValue =
        document.body.scrollTop || document.documentElement.scrollTop;
      let navbarColor = document.getElementById("toolbar");
      this.currentScrollValue = scrollValue;
      if (this.colorOnScroll > 0 && scrollValue > this.colorOnScroll) {
        this.extraNavClasses = `md-${this.type}`;
        navbarColor.classList.remove("md-transparent");
      } else {
        if (this.extraNavClasses) {
          this.extraNavClasses = "";
          navbarColor.classList.add("md-transparent");
        }
      }
    },
    scrollListener() {
      resizeThrottler(this.handleScroll);
    },
    scrollToElement() {
      let element_id = document.getElementById("downloadSection");
      if (element_id) {
        element_id.scrollIntoView({ block: "end", behavior: "smooth" });
      }
    },
    
    logout(){
      //reset all variables
      this.$store.commit('setVerify', false)
      this.$store.commit('setToken', null)
      this.$store.commit('setSearch', '?')
      this.$store.dispatch('setQParams',{
        sample:'',
        host_organism:'',
        virus_type:'',
        taxonomy:'',
        description:'',
        cultivar:'',
        verified: '',
        exclude_vitis: '',
        start_date: '',
        end_date: '',
        ordering: ''
      }) 
      //this.$store.commit('setQParams', '')
      // this.$store.state.token = null;
      // this.$store.state.can_verify = false;
      sessionStorage.clear();
      this.$router.push('/');
      console.log(this.$store.state.token)
    },


  },
  mounted() {
    document.addEventListener("scroll", this.scrollListener);
  },
  beforeDestroy() {
    document.removeEventListener("scroll", this.scrollListener);
  },
  created() { //calls methods

  }
};
</script>

