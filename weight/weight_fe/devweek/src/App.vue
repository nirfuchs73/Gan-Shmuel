<template>
  <div id="app">
    <BContainer fluid>
      <BRow>
        <BCol>
          <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
          <HelloWorld msg="Welcome to Gan Chaim!"/>
        </BCol>
      </BRow>
      <BRow>
        <BCard no-body>
          <BTabs card>

            <BTab title="Health" @click="checkHealth()">
              <GetHealth :health="health"></GetHealth>
            </BTab>

            <BTab title="Search in Weights" active>
              <GetWeightTable :urlPath="urlPath"></GetWeightTable>
            </BTab>

            <BTab title="Post a New Weight">
              <p>git!</p>
            </BTab>

            <BTab title="Tab 1">
              <p>git!</p>
            </BTab>
          </BTabs>
        </BCard>
      </BRow>
    </BContainer>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import {
  BContainer, BRow, BCol, BTabs, BTab, BCard,
} from 'bootstrap-vue';
import axios from 'axios';
import HelloWorld from './components/HelloWorld.vue';
import GetHealth from './components/GetHealth.vue';
import GetWeightTable from './components/GetWeightTable.vue';

@Component({
  components: {
    HelloWorld,
    BContainer,
    BRow,
    BCol,
    BTabs,
    BTab,
    BCard,
    GetHealth,
    GetWeightTable,
  },
})
export default class App extends Vue {
  private health: boolean = false;

  static getUrlPath() {
    // const url = new URL('api', window.document.location.href);
    // return url.href;
    return window.document.location.href;
  }

  private appUrlPath: string = App.getUrlPath(); // 'http://localhost:8090/';

  get urlPath() {
    return this.appUrlPath;
  }

  public checkHealth() {
    const url = new URL('health', this.urlPath);
    axios.get(url.href).then(
      (val) => {
        this.health = (val.status === 200); // && val.data.status === 200);
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
