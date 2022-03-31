<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Files</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Upload Files</button>
        <hr>
        <button type="button" class="btn btn-success btn-sm">Download Files</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">File</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>foo</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
            </tr>
          <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Merge</button>
                  <button type="button" class="btn btn-dark btn-sm">Split</button>
                  <button type="button" class="btn btn-info btn-sm">Start Processing</button>
          </div>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

// eslint-disable-next-line camelcase
const json_template = {
  'mission-params': {
    'mission-id': '',
    'mission-requester-email': '',
    'mission-email-notification-requested': false,
    'mission-translate': true,
    'mission-source-language': 'en',
    'mission-target-language': 'zh',
    'mission-file-list': [],
  },
  'split-params': {
  },
  'merge-params': {
  },
};
export default {
  name: 'Home',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    // eslint-disable-next-line camelcase,no-shadow
    getMissionID(json_template) {
      const path = 'http://localhost:8000/getmissionid';
      axios.get(path)
        .then((res) => {
          console.log(res);
          // eslint-disable-next-line no-param-reassign
          json_template['mission-params']['mission-id'] = res.data['mission-id'];
          console.log(json_template);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  created() {
    this.getMissionID(json_template);
  },
};
</script>
