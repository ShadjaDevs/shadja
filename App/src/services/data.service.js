import { ref } from "vue";

const zipCode = ref(0);
const searchRadius = ref(0);

export default function () {
  return {
    zipCode,
    searchRadius
  };
}
