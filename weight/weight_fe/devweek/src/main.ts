import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import App from './App.vue';
import store from './store';
// import Datetime from 'vue-datetime';


import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'vue-datetime/dist/vue-datetime.css';

Vue.use(BootstrapVue);
// Vue.use(Datetime);

Vue.config.productionTip = false;

new Vue({
  store,
  render: h => h(App),
}).$mount('#app');
