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
            <tr v-for="(file, index) in merge_split.files" :key="index">
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
                  <button type="button"
                          class="btn btn-warning btn-sm"
                          @click="onMerge()"
                          v-b-modal.merge-modal>Merge</button>
                  <button type="button" class="btn btn-dark btn-sm">Split</button>
                  <button type="button" class="btn btn-info btn-sm">Start Processing</button>
          </div>
          </tbody>
        </table>
      </div>
    </div>
    <!--UPLOAD-->
    <b-modal ref="uploadFileModal"
             id="file-modal"
             title="Upload Files"
            hide-footer>
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
    <!--MERGE-->
    <b-modal static ref="mergeModal"
             id="merge-modal"
             title="Merge Settings"
            hide-footer>
        <div class="container mt-5 mb-5">
          <div class="row">
            <div class="col mx-2 px-2 py-3 bg-light border rounded">
              <h6>File Pool</h6>
              <draggable class="draggable-list" :list="merge_split.pool" group="merge_split">
                <div v-for="(file, i) in merge_split.pool" :key="i">
                  <div class="bg-white mt-3 p-2 shadow border rounded">
                    <p>{{ file.name }}</p>
                  </div>
                </div>
              </draggable>
            </div>
            <div class="col mx-2 px-2 py-3 bg-light border rounded">
              <h6>In Progress</h6>
              <draggable class="draggable-list" :list="merge_split.inProgress" group="merge_split">
                <div v-for="(progress, i) in merge_split.inProgress" :key="i">
                  <div class="bg-white mt-3 p-2 shadow border rounded">
                    <p>{{ progress.name }}</p>
                  </div>
                </div>
              </draggable>
            </div>
            <div class="col mx-2 px-2 py-3 bg-light border rounded">
              <h6>Settings</h6>
              <div id="app">
                <div v-for="(progress, i) in merge_split.inProgress"
                     :key="i">
                  <p v-if="i===merge_split.merge_counter">
                    {{progress.name}}</p>
                </div>
                <b-form @submit="onSave">
                  <ul>
                    <li v-for="(input, index) in merge_split.merge_inputs" :key ="index">
                      <input type="text"
                             v-model="input.from"
                             class = "input-group">-
                      <input type="text"
                             v-model="input.to"
                             class = "input-group">
                      <button @click="deleteRow(index,merge_split.merge_inputs)"
                              class = "btn btn-outline-danger btn-sm">Delete</button>
                    </li>
                  </ul>
                  <button type="button"
                          @click="addRow(merge_split.merge_inputs)"
                          class = "btn btn-outline-primary btn-sm">Add Setting</button>
                  <button type="submit"
                          class = "btn btn-outline-success btn-sm">Save</button>
                  <button type="button"
                          @click="onFinishSetting"
                          class = "btn btn-success btn-sm">Finish Setting</button>
                </b-form>
              </div>
            </div>
          </div>
        </div>
    </b-modal>
  </div>
</template>

<style>
h6 {
  font-weight: 700;
}
.col {
  overflow: auto;
}
.draggable-list {
  min-height: 10vh;
}
.draggable-list > div {
  cursor: pointer;
}
</style>

<script>
import axios from 'axios';
import draggable from 'vuedraggable';
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
  components: {
    // eslint-disable-next-line vue/no-unused-components
    alert: Alert,
    draggable,
  },
  data() {
    return {
      merge_split: {
        merge_counter: 0,
        files: [],
        pool: [],
        inProgress: [],
        merge_inputs: [],
        merge_task: [],
        merge_task_all: [],
      },
      selectedFile: 0,
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
        this.merge_split.files.push(files_list[i]);
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
      this.merge_split.files.forEach((file) => {
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
          for (let i = 0; i < this.merge_split.files.length; i++) {
            json_template['mission-params']['mission-file-list'][i] = this.merge_split.files[i].name;
            this.merge_split.pool[i] = this.merge_split.files[i];
          }
          this.message = 'Files Uploaded!';
          this.showMessage = true;
        }
      });
    },
    // get Mission ID before mounting
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
          for (let i = 0; i < this.merge_split.files.length; i++) {
            if (this.merge_split.files[i].name === fileName) {
              this.merge_split.files.splice(i, 1);
              this.merge_split.pool.splice(i, 1);
            }
          }
          this.message = 'Files Removed!';
          this.showMessage = true;
        }
      });
    },
    // triggered when delete file button is hit
    onDeleteFile(file) {
      this.deleteFile(file.name);
    },
    // triggered when merge button is hit
    onMerge() {
      // eslint-disable-next-line no-plusplus
      for (let i = 0; i < this.merge_split.files.length; i++) {
        this.merge_split.pool[i] = this.merge_split.files[i];
      }
      this.merge_split.inProgress = [];
    },
    // add row to setting
    addRow(input) {
      input.push({
        from: '',
        to: '',
      });
    },
    // delete row from setting
    deleteRow(index, input) {
      input.splice(index, 1);
    },
    // save setting
    onSave(evt) {
      evt.preventDefault();
      try {
        // post request to the frontend server /upload
        this.saveSetting();
      } catch (err) {
        // eslint-disable-next-line no-console
        console.log(err);
      }
    },
    // post request to save settings
    saveSetting() {
      axios({
        method: 'post',
        url: 'http://localhost:3000/merge_save',
        data: {
          taskNum: this.merge_split.merge_counter,
          taskFile: this.merge_split.inProgress[this.merge_split.merge_counter].name,
          taskInput: this.merge_split.merge_inputs,
        },
      }).then((res) => {
        if (res.data.save_status === 'Merge Saved!') {
          this.merge_split.merge_task.push(res.data.save_data);
          this.merge_split.merge_counter += 1;
          this.merge_split.merge_inputs = [];
        }
      });
    },
    onFinishSetting() {
      this.$refs.mergeModal.hide();
      this.merge_split.merge_task_all.push(this.merge_split.merge_task);
      this.merge_split.merge_counter = 0;
      this.merge_split.merge_task = [];
    },
    onStartProcessing() {
      json_template['merge-params'] = this.merge_split.merge_task_all;
    },
  },
  created() {
    this.getMissionID(json_template);
  },
};
</script>
