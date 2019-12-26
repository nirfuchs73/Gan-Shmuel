<template>
  <BTr>
    <BTd>{{ cid }}</BTd>
    <BTd><span v-text="tara"></span></BTd>
  </BTr>
</template>

<script lang="ts">


import { Component, Prop, Vue } from 'vue-property-decorator';
import {
  BTr, BTd, BTableSimple, BTbody, BThead,
  BTfoot, BTh,
} from 'bootstrap-vue';
import axios from 'axios';
import { ErrorObject, GetWeightItemObject } from '@/lib';

@Component({
  components: {
    BTableSimple, BTbody, BThead, BTr, BTd,
  },
})
export default class GetWeightContainerItem extends Vue {
  @Prop() private urlPath: string = window.document.location.href;

  @Prop() private from!: string;

  @Prop() private to!: string;

  @Prop() private cid!: string;

  private pTara: number | string = 'unknown';

  get tara() : number | string {
    if (this.pTara === 'unknown') {
      this.getContainerData();
    }
    return this.pTara;
  }

  getContainerData() {
    const p = '/item/'.concat(this.cid);
    const url = new URL(p, this.urlPath);
    if (this.from && this.from !== '') {
      url.searchParams.append('from', this.from);
    }
    if (this.to && this.to !== '') {
      url.searchParams.append('to', this.to);
    }
    axios.get(url.href).then(({ data }) => {
      if (data.tara) {
        this.pTara = data.tara;
      }
    }).catch((res) => {
      const { response } = res;
      this.pTara = 'unknown';
    });
  }
}
</script>
