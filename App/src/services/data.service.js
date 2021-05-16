import { ref } from "vue";

const pinCode = ref(0);
const searchRadius = ref(0);

export default function () {
  return {
    pinCode,
    searchRadius
  };
}
