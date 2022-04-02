<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>PDF-Slicer</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
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
                  <button type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteFile(file)">Delete</button>
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
      <b-form enctype="multipart/form-data"
              @submit="onSubmit"
              @reset="onReset">
        <div class="dropbox">
          <input type="file" multiple
                 ref="uploadedFiles"
                 @change="handleFileChange($event)"
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
import Alert from './Alert.vue';

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
      message: '',
      showMessage: false,
    };
  },
  methods: {
    // This is for uploading modal when selecting files
    handleFileChange(evt) {
      this.selectedFile = evt.target.files.length;
      // eslint-disable-next-line camelcase
      const files_list = this.$refs.uploadedFiles.files;
      // eslint-disable-next-line guard-for-in,no-restricted-syntax,no-plusplus
      for (let i = 0; i < files_list.length; i++) {
        this.files.push(files_list[i]);
      }
    },
    // handle click event for upload button
    handleClickEvent() {
      this.selectedFile = 0;
    },
    // submit form
    onSubmit(evt) {
      evt.preventDefault();
      const formData = new FormData();
      this.files.forEach((file) => {
        formData.append('file', file);
      });
      this.$refs.uploadFileModal.hide();
      try {
        // post request to the frontend server /upload
        this.uploadFiles(formData);
      } catch (err) {
        // eslint-disable-next-line no-console
        console.log(err);
      }
    },
    // reset form
    onReset(evt) {
      evt.preventDefault();
      this.selectedFile = 0;
    },
    // post request to frontend server to create the directory
    // eslint-disable-next-line camelcase
    createMission_Dir(mission_id) {
      axios({
        method: 'post',
        url: 'http://localhost:3000/mkdir',
        data: {
          id: mission_id,
        },
      });
    },
    // upload files by frontend server
    uploadFiles(formData) {
      axios({
        method: 'post',
        url: 'http://localhost:3000/upload',
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }).then((res) => {
        if (res.data.upload_status === 'Upload File!') {
          // eslint-disable-next-line no-plusplus
          for (let i = 0; i < this.files.length; i++) {
            json_template['mission-params']['mission-file-list'][i] = this.files[i].name;
          }
          this.message = 'Files Uploaded!';
          this.showMessage = true;
        }
      });
    },
    // eslint-disable-next-line camelcase,no-shadow
    getMissionID(json_template) {
      const path = 'http://localhost:8000/getmissionid';
      axios.get(path)
        .then((res) => {
          // eslint-disable-next-line no-param-reassign
          json_template['mission-params']['mission-id'] = res.data['mission-id'];
          this.createMission_Dir(res.data['mission-id']);
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.log(error);
        });
    },
    // delete uploaded files
    deleteFile(fileName) {
      axios({
        method: 'post',
        url: 'http://localhost:3000/delete',
        data: {
          deleteName: fileName,
        },
      }).then((res) => {
        if (res.data.delete_status === 'Delete!') {
          // eslint-disable-next-line no-plusplus
          for (let i = 0; i < this.files.length; i++) {
            if (this.files[i].name === fileName) {
              this.files.splice(i, 1);
              console.log(i);
            }
          }
          console.log(this.files);
          this.message = 'Files Removed!';
          this.showMessage = true;
        }
      });
    },
    onDeleteFile(file) {
      this.deleteFile(file.name);
    },
  },
  components: {
    // eslint-disable-next-line vue/no-unused-components
    alert: Alert,
  },
  created() {
    this.getMissionID(json_template);
  },
};
</script>
