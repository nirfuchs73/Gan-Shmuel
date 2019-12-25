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
            <input v-model="fromDate" type="date" class="form-control">
            <!-- <BFormInput :type="time" v-model="fromTime"></BFormInput> -->
            <input v-model="fromTime" type="time" class="form-control">

          </BInputGroup>

          <!-- To Date Field -->
          <BInputGroup>
            <template v-slot:prepend>
              <input type="checkbox" v-model="toUsing" class="form-control">
              <BInputGroupText >To Date</BInputGroupText>
            </template>
            <!-- <BFormInput :type="" v-model=""></BFormInput> -->
            <input v-model="toDate" type="date" class="form-control">
            <!-- <BFormInput :type="time" v-model="fromTime"></BFormInput> -->
            <input v-model="toTime" type="time" class="form-control">

          </BInputGroup>

          <!-- Filter Field(s) -->
          <BInputGroup>
            <BFormSelect multiple :options="fops" v-model="filters"></BFormSelect>
          </BInputGroup>

          <b-button variant="primary" @click="checkWeights">Get Weights!</b-button>

        </BForm>
      </BCol>
    </BRow>

    <!-- Search Results as a Table Row -->
    <BRow>
    </BRow>
  </BContainer>
</template>


<script lang="ts">


import { Component, Prop, Vue } from 'vue-property-decorator';
import {
  BForm, BFormInput, BContainer, BRow, BCol, BInputGroup, BInputGroupPrepend,
  BInputGroupAppend, BInputGroupText, BFormSelect,
} from 'bootstrap-vue';
import axios from 'axios';

  @Component(
    {
      components: {
        BForm, BFormInput, BContainer, BRow, BCol,
      },
    },
  )
export default class GetWeightTable extends Vue {
    @Prop() private items!: any[];

    @Prop() private fromUsing!: boolean;

    @Prop() private fromDate!: string;

    @Prop() private fromTime!: string;

    @Prop() private toUsing!: boolean;

    @Prop() private toDate!: string;

    @Prop() private toTime!: string;

    @Prop() private filters: string[] = ['in', 'out', 'none'];

    @Prop() private fops: object[] = [
      { value: 'in', text: 'Weight On Entry' },
      { value: 'out', text: 'Weight On Departure' },
      { value: 'none', text: 'Other' },
    ];

    private checkWeights() {
      this.items = [];
    }
}

</script>
