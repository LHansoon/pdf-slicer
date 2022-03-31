<template>
  <div>
    <p>{{ msg }}</p>
    <button>Update Files</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Home',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:8000/getmissionid';
      axios.get(path)
        .then((res) => {
          console.log(res);
          this.msg = res.data['mission-id'];
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
