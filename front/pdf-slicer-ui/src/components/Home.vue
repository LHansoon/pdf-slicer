<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>PDF-Slicer</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm"
                @click="handleClickEvent()" v-b-modal.file-modal>
          Upload Files</button>
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
            <tr v-for="(file, index) in files" :key="index">
              <td>{{file.name}}</td>
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
    <b-modal ref="uploadFileModal"
            id="file-modal"
            title="Upload Files"
            hide-footer>
      <!--UPLOAD-->
      <b-form enctype="multipart/form-data">
        <div class="dropbox">
          <input type="file" multiple
                 @change="handleFileChange($event)"
                 @submit="onSubmit()"
                 @reset.prevent="onReset()"
                 class="btn btn-primary btn-sms"
                 placeholder="Upload Files"/>
          <p>You have selected {{selectedFile}} files!</p>
          <b-button type="submit" class="btn btn-success btn-sm">Submit</b-button>
          <b-button type="reset" class="btn btn-danger btn-sm">Reset</b-button>
        </div>
      </b-form>
    </b-modal>
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
      selectedFile: 0,
      files: [],
    };
  },
  methods: {
    // This is for uploading modal when selecting files
    handleFileChange(evt) {
      this.selectedFile = evt.target.files.length;
    },
    // handle click event for upload button
    handleClickEvent() {
      this.selectedFile = 0;
    },
    // submit form
    onSubmit() {

    },
    // reset form
    onReset() {
      this.selectedFile = 0;
    },
    // post request to frontend server to create the directory
    createMission_Dir() {

    },
    // upload files by frontend server
    uploadFiles() {

    },
    // eslint-disable-next-line camelcase,no-shadow
    getMissionID(json_template) {
      const path = 'http://localhost:8000/getmissionid';
      axios.get(path)
        .then((res) => {
          console.log(res);
          // eslint-disable-next-line no-param-reassign
          json_template['mission-params']['mission-id'] = res.data['mission-id'];
          // console.log(json_template);
          this.files = json_template['mission-params']['mission-file-list'];
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
