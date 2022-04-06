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
                          @click="onMerge_Split"
                          v-b-modal.merge-modal>Merge</button>
                  <button type="button"
                          class="btn btn-dark btn-sm"
                          @click="onMerge_Split"
                          v-b-modal.split-modal>Split</button>
                  <button type="button"
                          class="btn btn-secondary btn-sm"
                          v-b-modal.translate-modal>Translate</button>
                  <button type="button"
                          class="btn btn-info btn-sm"
                          v-b-modal.processing-modal>Start Processing</button>
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
             size="xl"
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
              <div id="merge_app">
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
    <!--Split-->
    <b-modal static ref="splitModal"
             id="split-modal"
             title="Split Settings"
             size="xl"
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
              <div id="split_app">
                <div v-for="(progress, i) in merge_split.inProgress"
                     :key="i">
                  <p v-if="i===merge_split.split_counter">
                    {{progress.name}}</p>
                </div>
                <b-form @submit="onSaveSplit">
                  <ul>
                    <li v-for="(input, index) in merge_split.split_inputs" :key ="index">
                      <input type="text"
                             v-model="input.from"
                             class = "input-group">-
                      <input type="text"
                             v-model="input.to"
                             class = "input-group">
                      <button @click="deleteRow(index,merge_split.split_inputs)"
                              class = "btn btn-outline-danger btn-sm">Delete</button>
                    </li>
                  </ul>
                  <button type="button"
                          @click="addRow(merge_split.split_inputs)"
                          class = "btn btn-outline-primary btn-sm">Add Setting</button>
                  <button type="submit"
                          class = "btn btn-outline-success btn-sm">Save</button>
                  <button type="button"
                          @click="onFinishSettingSplit"
                          class = "btn btn-success btn-sm">Finish Setting</button>
                </b-form>
              </div>
            </div>
          </div>
        </div>
    </b-modal>
    <!--Translate-->
    <b-modal static ref="translateModal"
             id="translate-modal"
             title="Translate Settings"
             size="xl"
            hide-footer>
        <div class="container mt-5 mb-5">
          <div class="row">
            <form @submit = "onSubmitTranslate">
              <div class="col mx-2 px-2 py-3 bg-light border rounded">
                <h6>Source Language</h6>
                  <select v-model="translate.source_selected">
                    <option disabled value="">Please select one</option>
                    <option value="en">en</option>
                    <option value="ar">ar</option>
                    <option value="cs">cs</option>
                    <option value="de">de</option>
                    <option value="es">es</option>
                    <option value="fr">fr</option>
                    <option value="it">it</option>
                    <option value="ja">ja</option>
                    <option value="pt">pt</option>
                    <option value="ru">ru</option>
                    <option value="tr">tr</option>
                    <option value="zh">zh</option>
                    <option value="zh-TW">zh-TW</option>
                  </select>
              </div>
              <div class="col mx-2 px-2 py-3 bg-light border rounded">
                <h6>Target Language</h6>
                  <select v-model="translate.target_selected">
                    <option disabled value="">Please select one</option>
                    <option value="en">en</option>
                    <option value="ar">ar</option>
                    <option value="cs">cs</option>
                    <option value="de">de</option>
                    <option value="es">es</option>
                    <option value="fr">fr</option>
                    <option value="it">it</option>
                    <option value="ja">ja</option>
                    <option value="pt">pt</option>
                    <option value="ru">ru</option>
                    <option value="tr">tr</option>
                    <option value="zh">zh</option>
                  </select>
              </div>
              <button type="submit"
                      class = "btn btn-outline-success btn-sm">Submit</button>
            </form>
          </div>
        </div>
    </b-modal>
    <!--Processing-->
    <b-modal ref="processingModal"
             id="processing-modal"
             title="Enter Your Email"
             size="xl"
            hide-footer>
      <b-form enctype="multipart/form-data"
              @submit="onStartProcessing">
        <p>Do you want to be notified via email?</p>
        <div class="input-group">
          <input type="text"
                 @change = "onHandleEmail"
                 placeholder="Please Enter your Email..."/>
        </div>
        <b-button type="submit" class="btn btn-success btn-sm">Submit</b-button>
      </b-form>
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
    'mission-translate': false,
    'mission-source-language': '',
    'mission-target-language': '',
    'mission-file-list': [],
  },
  'split-params': {
  },
  'merge-params': [
  ],
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
        merge_task_no: 0,
        merge_counter: 0,
        files: [],
        pool: [],
        inProgress: [],
        merge_inputs: [],
        merge_task: {},
        merge_task_all: {},
        split_counter: 0,
        split_inputs: [],
        split_task: {},
      },
      translate: {
        source_selected: '',
        target_selected: '',
      },
      email: '',
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
      this.getMissionID(json_template);
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
        url: 'http://express:3000/mkdir',
        data: {
          id: mission_id,
        },
      });
    },
    // upload files by frontend server
    uploadFiles(formData) {
      axios({
        method: 'post',
        url: 'http://express:3000/upload',
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
        url: 'http://express:3000/delete',
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
    onMerge_Split() {
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
        url: 'http://express:3000/merge_save',
        data: {
          taskInput: this.merge_split.merge_inputs,
        },
      }).then((res) => {
        if (res.data.save_status === 'Merge Saved!') {
          this.merge_split.merge_task[this.merge_split.merge_counter] = {
            'file-name': this.merge_split.inProgress[this.merge_split.merge_counter].name,
            'inner-merge-order': {},
          };
          // eslint-disable-next-line no-plusplus
          for (let i = 0; i < this.merge_split.merge_inputs.length; i++) {
            this.merge_split.merge_task[this.merge_split.merge_counter]['inner-merge-order'][i] = {
              // eslint-disable-next-line radix,max-len
              from: parseInt(res.data.save_data_from[0][i]), to: parseInt(res.data.save_data_to[0][i]),
            };
          }
          this.merge_split.merge_counter += 1;
          this.merge_split.merge_inputs = [];
        }
      });
    },
    onFinishSetting() {
      this.$refs.mergeModal.hide();
      json_template['merge-params'].push(this.merge_split.merge_task);
      this.merge_split.merge_task_no += 1;
      this.merge_split.merge_counter = 0;
      this.merge_split.merge_task = {};
      this.message = 'Merging Mission Added!';
      this.showMessage = true;
    },
    onSaveSplit(evt) {
      evt.preventDefault();
      try {
        // post request to the frontend server /upload
        this.saveSplitSetting();
      } catch (err) {
        // eslint-disable-next-line no-console
        console.log(err);
      }
    },
    saveSplitSetting() {
      axios({
        method: 'post',
        url: 'http://express:3000/split_save',
        data: {
          taskInput: this.merge_split.split_inputs,
        },
      }).then((res) => {
        if (res.data.save_status === 'Split Saved!') {
          json_template['split-params'][this.merge_split.inProgress[this.merge_split.split_counter].name] = [];
          // eslint-disable-next-line no-plusplus
          for (let i = 0; i < this.merge_split.split_inputs.length; i++) {
            json_template['split-params'][this.merge_split.inProgress[this.merge_split.split_counter].name].push({
              // eslint-disable-next-line radix
              'part-id': i, from: parseInt(res.data.save_data_from[0][i]), to: parseInt(res.data.save_data_to[0][i]),
            });
          }
          this.merge_split.split_counter += 1;
          this.merge_split.split_inputs = [];
        }
      });
    },
    onFinishSettingSplit() {
      this.$refs.splitModal.hide();
      this.merge_split.split_counter = 0;
      this.message = 'Splitting Mission Added!';
      this.showMessage = true;
    },
    onStartProcessing(evt) {
      evt.preventDefault();
      this.$refs.processingModal.hide();
      json_template['mission-params']['mission-requester-email'] = this.email;
      json_template['mission-params']['mission-email-notification-requested'] = true;
      const path = 'http://localhost:8000/postrequest';
      axios.post(path, json_template).then((res) => {
        console.log(res);
      });
    },
    onSubmitTranslate(evt) {
      evt.preventDefault();
      this.$refs.translateModal.hide();
      json_template['mission-params']['mission-translate'] = true;
      json_template['mission-params']['mission-source-language'] = this.translate.source_selected;
      json_template['mission-params']['mission-target-language'] = this.translate.target_selected;
    },
    onHandleEmail(evt) {
      this.email = evt.target.value;
    },
  },
  created() {
  },
};
</script>
