<template>

</template>

<script lang="ts">

import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class GetWeightItem extends Vue {
  @Prop() private direction!: string;

  @Prop() private id!: number;

  @Prop() private produce!: string;

  @Prop() private neto!: string | number;

  @Prop() private bruto!: number;

  @Prop() private containers!: string[];

}

// {
//       'id' : t_trans.get('id'),
//       "direction": t_trans.get('direction'),
//       "bruto": t_trans.get('bruto'), # assuming that bruto is stored as kg..
//       "neto": neto_res,
//       "produce": t_trans.get('produce'),
//       "containers": conts
// }

</script>
