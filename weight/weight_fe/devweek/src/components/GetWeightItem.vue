<template>
  <BTr>
    <BTd>{{ item.id }}</BTd>
    <BTd>{{ item.direction }}</BTd>
    <BTd>{{ item.produce }}</BTd>
    <BTd>{{ item.bruto }}</BTd>
    <BTd>{{ item.neto }}</BTd>
    <BTd>
      <BTableSimple>
        <BThead>
            <BTr>
              <BTh>Container ID</BTh>
              <BTh>Container Weight</BTh>
            </BTr>
          </BThead>
          <BTbody>
            <GetWeightContainerItem v-for="(cid, idx) in item.containers" :key="idx"
              :cid="cid" :urlPath="urlPath" :from="from" :to="to"
            ></GetWeightContainerItem>
          </BTbody>
      </BTableSimple>
    </BTd>
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
import GetWeightContainerItem from './GetWeightContainerItem.vue';

@Component({
  components: {
    BTr, BTd, GetWeightContainerItem,
  },
})
export default class GetWeightItem extends Vue {
  @Prop() private urlPath: string = window.document.location.href;

  @Prop() private item!: GetWeightItemObject;

  @Prop() private from!: string;

  @Prop() private to!: string;

  // private conWgt: Map<string, number | null> = new Map<string, number | null>();

  // getCntWeght(cid:string): number | null | undefined {
  //   if (this.conWgt.has(cid)) {
  //     return this.conWgt.get(cid);
  //   }
  //   return null;
  // }

  // get myReactiveCW() : (cid:string, def:string) => string | number {
  //   return (cid:string, def:string = '') => this.getContainerData(cid, def);
  // }

  // setCntWeght(cid:string, tara: number | null) {
  //   this.conWgt.set(cid, tara);
  // }

  // getContainerData(cid:string, def:string = '') {
  //   const p = '/item/'.concat(cid);
  //   const url = new URL(p, this.urlPath);
  //   if (this.from && this.from !== '') {
  //     url.searchParams.append('from', this.from);
  //   }
  //   if (this.to && this.to !== '') {
  //     url.searchParams.append('to', this.to);
  //   }
  //   axios.get(url.href).then(({ data }) => {
  //     if (data.tara) {
  //       this.setCntWeght(cid, data.tara);
  //     }
  //   }).catch((res) => {
  //     const { response } = res;
  //     this.setCntWeght(cid, null);
  //   });
  //   const tara = this.getCntWeght(cid);
  //   return tara !== null && tara !== undefined ? tara : def;
  // }
}
</script>
