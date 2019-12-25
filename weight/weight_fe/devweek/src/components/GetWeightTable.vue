<template>
  <BContainer>
    <!-- title search bar row -->
    <BRow>
      <BCol>
        <BForm :inline="true" :novalidate="true">

          <!-- From Date Field -->
          <BInputGroup></BInputGroup>

          <!-- To Date Field -->
          <BInputGroup></BInputGroup>

          <!-- Filter Field(s) -->
          <BInputGroup></BInputGroup>

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
  BInputGroupAppend
} from 'bootstrap-vue';

@Component(
  {
    components: {
      BForm, BFormInput, BContainer, BRow, BCol
    }
  }
)
export default class GetWeightTable extends Vue {
  @Prop() private items!: any[];

</script>
