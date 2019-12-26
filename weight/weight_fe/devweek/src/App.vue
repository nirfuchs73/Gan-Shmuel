<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Gan Chaim!"/>
    <BCard no-body>
      <BTabs card>

        <BTab title="Health" @click="checkHealth()">
          <GetHealth :health="health"></GetHealth>
        </BTab>

        <BTab title="Weights" active>
          <GetWeightTable></GetWeightTable>
        </BTab>


        <BTab title="Tab 1">
          <p>git!</p>
        </BTab>
      </BTabs>
    </BCard>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { BTabs, BTab, BCard } from 'bootstrap-vue';
import axios from 'axios';
import HelloWorld from './components/HelloWorld.vue';
import GetHealth from './components/GetHealth.vue';
import GetWeightTable from './components/GetWeightTable.vue';

@Component({
  components: {
    HelloWorld, BTabs, BTab, BCard, GetHealth, GetWeightTable,
  },
})
export default class App extends Vue {
  private health: boolean = false;

  public checkHealth() {
    axios.get('/health').then(
      (val) => {
        this.health = (val.status === 200 && val.data.status === 200);
      },
      (res) => {
        this.health = false;
      },
    );
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
