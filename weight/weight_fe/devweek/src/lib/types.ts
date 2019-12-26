

export interface ErrorObject {
  status: number;
  message: string;
  response: object;
  request: object;
}

export interface GetWeightItemObject {
 id: number;
 direction: string;
 produce: string;
 bruto: number;
 neto: string | number;
 containers: string[];
}
