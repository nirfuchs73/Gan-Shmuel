<template>
  <img v-if="health" src="../assets/approved.png" alt="The Server is GOOD!">
  <img v-else src="../assets/cancel.png" alt="The Server is DOWN!">
</template>

<script lang="ts">

import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class GetWeightItem extends Vue {
  @Prop() private health!:boolean;
}
</script>
