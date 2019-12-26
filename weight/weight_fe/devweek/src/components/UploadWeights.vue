<template>
  <BContainer>
    <BRow>
      <BCol>
        <h2>Upload a new Weights File</h2>
        <BForm>

        </BForm>
      </BCol>
    </BRow>
  </BContainer>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import {
  BContainer, BRow, BCol, BFormFile, BForm,
} from 'bootstrap-vue';

@Component
export default class UploadWeights extends Vue {
  @Prop() private msg!: string;
}
</script>
