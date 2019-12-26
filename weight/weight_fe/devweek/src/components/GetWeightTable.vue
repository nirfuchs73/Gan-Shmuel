<template>
  <BContainer>
    <!-- title search bar row -->
    <BRow>
      <BCol>
        <BForm :inline="true" :novalidate="true">

          <!-- From Date Field -->
          <BInputGroup>
            <template v-slot:prepend>
              <input type="checkbox" v-model="fromUsing" class="form-control">
              <BInputGroupText >From Date</BInputGroupText>
            </template>
            <!-- <BFormInput :type="" v-model=""></BFormInput> -->
            <!-- <input v-model="fromDate" type="date" class="form-control"> -->
            <!-- <BFormInput :type="time" v-model="fromTime"></BFormInput> -->
            <!-- <input v-model="fromTime" type="time" class="form-control"> -->
            <BCollapse v-model="fromUsing">
              <Datetime v-model="from" type="datetime"></Datetime>
            </BCollapse>

          </BInputGroup>

          <!-- To Date Field -->
          <BInputGroup>
            <template v-slot:prepend>
              <input type="checkbox" v-model="toUsing" class="form-control">
              <BInputGroupText >To Date</BInputGroupText>
            </template>
            <!-- <BFormInput :type="" v-model=""></BFormInput> -->
            <!-- <input v-model="toDate" type="date" class="form-control"> -->
            <!-- <BFormInput :type="time" v-model="fromTime"></BFormInput> -->
            <!-- <input v-model="toTime" type="time" class="form-control"> -->
            <BCollapse v-model="toUsing">
              <Datetime v-model="to" type="datetime"></Datetime>
            </BCollapse>

          </BInputGroup>

          <!-- Filter Field(s) -->
          <BInputGroup>
            <template v-slot:prepend>
              <input type="checkbox" v-model="filtersUsing" class="form-control">
              <BInputGroupText >Filters</BInputGroupText>
            </template>

            <BCollapse v-model="filtersUsing">
              <BFormSelect multiple :options="fops" v-model="filters"></BFormSelect>
            </BCollapse>
          </BInputGroup>

          <b-button variant="primary" @click="checkWeights">Get Weights!</b-button>

        </BForm>
      </BCol>
    </BRow>

    <!-- Search Results as a Table Row -->
    <BRow>
      <BCol>
        <BCollapse :visible="items.length > 0">
          <BTableSimple>
            <BThead>
              <BRow>
                <BTh>Session ID</BTh>
                <BTh>Direction</BTh>
                <BTh>Produce</BTh>
                <BTh>Bruto</BTh>
                <BTh>Neto</BTh>
                <BTh :colspan="2">Containers</BTh>
              </BRow>
            </BThead>
            <BTbody>
              <GetWeightItem v-for="(item, idex) in getItems"
                :key="idex" :item="item" :from="from" :to="to"
                :urlPath="appUrlPath"
              ></GetWeightItem>
            </BTbody>
            <BTfoot>
              <BRow>
                <BTh :colspan="5"></BTh>
                <BTh>Container ID</BTh>
                <BTh>Container Weight</BTh>
              </BRow>
              <BRow>
                <BTh>Session ID</BTh>
                <BTh>Direction</BTh>
                <BTh>Produce</BTh>
                <BTh>Bruto</BTh>
                <BTh>Neto</BTh>
                <BTh :colspan="2">Containers</BTh>
              </BRow>
            </BTfoot>
          </BTableSimple>
        </BCollapse>
        <BCollapse :visible="error.status > 0">
          <BCard :bg-variant="errColor">
            <BCardText> {{ error.message }} </BCardText>
          </BCard>
        </BCollapse>
      </BCol>
    </BRow>
  </BContainer>
</template>


<script lang="ts">


import {
  Component, Prop, PropSync, Vue,
} from 'vue-property-decorator';
import {
  BForm, BFormInput, BContainer, BRow, BCol,
  BInputGroup, BInputGroupPrepend, BCollapse,
  BInputGroupAppend, BInputGroupText, BFormSelect,
  BCard, BCardText, BTableSimple, BTbody, BThead,
  BTfoot, BTr, BTd, BTh,
} from 'bootstrap-vue';
import { Datetime } from 'vue-datetime';
import { DateTime as DtFormater } from 'luxon';
import axios, { AxiosError } from 'axios';
// import * as url from 'url';
import GetWeightItem from './GetWeightItem.vue';
import { ErrorObject, GetWeightItemObject } from '@/lib';


  @Component(
    {
      components: {
        BForm,
        BFormInput,
        BContainer,
        BRow,
        BCol,
        Datetime,
        BCollapse,
        GetWeightItem,
        BCard,
        BCardText,
        BTableSimple,
        BTbody,
        BThead,
        BTfoot,
        BTr,
        BTd,
        BTh,
      },
    },
  )
export default class GetWeightTable extends Vue {
  // @PropSync('items', {}) itemsSync!: any[];

  @Prop() private urlPath!: string;

  get appUrlPath(): string {
    return this.urlPath;
  }

  private pItems : GetWeightItemObject[] = [];

  get items() : GetWeightItemObject[] {
    return this.pItems;
  }

  set items(val:GetWeightItemObject[]) {
    this.pItems = val;
  }

  // @PropSync('error', {}) errorSync!: AxiosError;
  private pError : ErrorObject = {
    message: '',
    status: 0,
    response: {},
    request: {},
  };

  get error() : ErrorObject {
    return this.pError;
  }

  set error(val:ErrorObject) {
    this.pError = val;
  }

  // static data(): object {
  //   return {
  //     items: [],
  //     error: null,
  //     fromUsing: false,
  //     from: '',
  //     toUsing: false,
  //     to: '',
  //     filtersUsing: false,
  //     filters: ['in', 'out', 'none'],
  //   };
  // }

  get getError(): Object {
    if (this.hasError) {
      return this.error;
    }
    return {
      status: 0,
      message: '',
      response: {},
      request: {},
    };
  }

  get hasItems(): boolean {
    return this.items !== undefined && this.items.length > 0;
  }

  get getItems(): GetWeightItemObject[] {
    if (this.items !== null && this.items !== null) {
      return this.items;
    }
    return [];
  }

  get hasError(): boolean {
    return this.error.status > 0;
  }

  get errColor(): string {
    let clr = 'bg-transparent';
    if (this.hasError) {
      if (this.error.status >= 400 && this.error.status < 500) {
        clr = 'bg-warning';
      } else if (this.error.status >= 500 && this.error.status < 600) {
        clr = 'bg-danger';
      }
    }
    return clr;
  }

  // @PropSync('fromUsing', { type: Boolean }) fromUsingSync!: boolean;
  // @Prop() fromUsing!: boolean;

  private pFromUsing: boolean = false;

  get fromUsing(): boolean {
    return this.pFromUsing;
  }

  set fromUsing(val:boolean) {
    this.pFromUsing = val;
  }

  // @Prop() private fromDate!: string;

  private pFrom: string = '';

  get from() {
    return this.pFrom;
  }

  set from(val: string) {
    this.pFrom = val;
  }

  // @PropSync('from', { type: String }) fromSync!: string;

  // @Prop() private fromTime!: string;

  // @PropSync('toUsing', { type: Boolean }) toUsingSync!: boolean;

  // @PropSync('to', { type: String }) toSync!: string;

  private pToUsing : boolean = false;

  get toUsing() : boolean {
    return this.pToUsing;
  }

  set toUsing(val:boolean) {
    this.pToUsing = val;
  }

  private pTo : string = '';

  get to() : string {
    return this.pTo;
  }

  set to(val:string) {
    this.pTo = val;
  }

  // @Prop() private toDate!: string;

  // @Prop() private toTime!: string;

  // @PropSync('filtersUsing', { type: Boolean }) filtersUsingSync!: boolean;

  private pFiltersUsing : boolean = false;

  get filtersUsing(): boolean {
    return this.pFiltersUsing;
  }

  set filtersUsing(val:boolean) {
    this.pFiltersUsing = val;
  }

  // @PropSync('filters', {}) filtersSync: string[] = ['in', 'out', 'none'];

  private pFilters : string[] = ['in', 'out', 'none'];

  get filters() : string[] {
    return this.pFilters;
  }

  set filters(val:string[]) {
    this.pFilters = val;
  }

  fops: object[] = [
    { value: 'in', text: 'Weight On Entry' },
    { value: 'out', text: 'Weight On Departure' },
    { value: 'none', text: 'Other' },
  ];

  checkWeights() {
    this.items = [];
    // const dtf = new DtFormater();
    this.error = {
      message: '',
      status: 0,
      response: {},
      request: {},
    };
    const url = new URL('/weight', this.appUrlPath);
    if (this.fromUsing) {
      url.searchParams.append('from', DtFormater.fromISO(this.from).toFormat('yyyyMMddhhmmss'));
    }
    if (this.toUsing) {
      url.searchParams.append('to', DtFormater.fromISO(this.to).toFormat('yyyyMMddhhmmss'));
    }
    if (this.filters) {
      const filters = this.filters.join(',');
      url.searchParams.append('filter', filters);
    }
    axios.get(url.href).then((val) => {
      if (val.data.length > 0) {
        this.items = val.data;
      }
    }).catch((err) => {
      if (err.response) {
        this.error.status = err.response.status;
        this.error.message = err.message;
        this.error.response = err.response;
        this.error.request = err.request;
      }
    });
  }
}

</script>
