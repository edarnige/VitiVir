<template>
  <div>
    <h4 v-if="totalResults !=0">{{totalResults}} entries</h4>

   <div class="md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25">
    <md-table component-name="pagination" class="pagination pagination-primary">
      <md-table-row>
        <md-table-head>query id</md-table-head>
        <md-table-head>evalue</md-table-head>
        <md-table-head>query length</md-table-head>
        <md-table-head>percent id</md-table-head>
        <md-table-head>verified</md-table-head>
      </md-table-row>

      <md-table-row @click="toDetail(entry)" v-for="entry in entries" v-bind:key="entry.entry_id">
        <md-table-cell v-if="entry.blastrps">{{ entry.query_id }}</md-table-cell> <!--may need double "if" if missing data -->
        <md-table-cell v-else> </md-table-cell>

        <md-table-cell>{{ entry.blastrps.evalue}}</md-table-cell>

        <md-table-cell v-if="entry.blastx">{{ entry.blastx.query_length }}</md-table-cell>
        <md-table-cell v-else> </md-table-cell>

        <md-table-cell v-if="entry.blastx">{{ entry.blastx.percent_identity }}</md-table-cell>
        <md-table-cell v-else> </md-table-cell>

        <md-table-cell> <i v-if="entry.verified==true" class="fas fa-check-circle"></i></md-table-cell>
      </md-table-row>
    </md-table>
   
    <pagination 
      type="primary"      
      :total="totalResults" 
      @input="updatePage"
      :value="currentPage"
      ><!--props passed to child (pagination) :prop--> 
    </pagination>

   </div>

  </div>
</template>


<script>
import axios from 'axios';
import {Pagination} from '@/components'

export default {
  name: 'ListEntries',
  components: {
    Pagination

  },
  data() {
    return {
      entries : [],
      totalResults: 0,
      defaultPagination: 1,
      totalPages: 1,
      currentPage: 1,
    }
  },

  methods: {
    getEntries() {
      this.$Progress.start()
      axios.get(`${process.env.VUE_APP_API_HOST}/api/data/entries/` + this.$store.state.search_q+"&page=1", {
        headers: {
          'Authorization': 'Token ' + this.$store.state.token //this.token
        }
      })
      .then(res => {
        this.$Progress.finish()
        this.entries = res.data.results
        this.totalResults = res.data.count
        })
      .catch(err =>{
        this.$Progress.fail()
        console.log(err);
      })
    },

    toDetail(entry){
      const entry_id = entry.entry_id
      this.$router.push({name: 'entrydetail', params: {entry_id}})
    },

    getSearch(){ //same as getEntries, delete one?
    //console.log("Entering getSearch")
      this.$Progress.start()
      this.currentPage = 1
      //console.log("setting current page", this.currentPage)
      axios.get(`${process.env.VUE_APP_API_HOST}/api/data/entries/`+this.$store.state.search_q+"&page=1", {
        headers: {
          'Authorization': 'Token ' + this.$store.state.token
        }
      })
      .then(res => {
        this.$Progress.finish()
        this.entries = res.data.results
        this.totalResults = res.data.count
      })
      .catch(err => {
        this.$Progress.fail()
        console.log(err);
      })

    },

    updatePage(item){
      this.$Progress.start()
      this.currentPage = item

      axios.get(`${process.env.VUE_APP_API_HOST}/api/data/entries/`+this.$store.state.search_q+"&page="+item, {
        headers: {
          'Authorization': 'Token ' + this.$store.state.token
        }
      })
      .then(res => {
        this.$Progress.finish()
        this.entries = res.data.results
        this.totalResults = res.data.count
        })
      .catch(err => {
        this.$Progress.fail()
        console.log(err)
        })
    }
    
    },

    created() { //calls methods
      this.getEntries(); //getSeatch();
    },


};
</script>

<style >
.fa-check-circle{
  color:  #4caf50;
}

</style>
