const express = require('express');
const cors = require('cors');
const fs = require('fs');
const bodyParser = require('body-parser')
const busboy = require('connect-busboy');
const request = require('request');

const app = express();
app.use(cors());
app.use(busboy());
const port = '3000' || process.env.PORT;

app.use(bodyParser.json())

app.use(
    bodyParser.urlencoded({
        extended: false,
    })
);


let mission_id = '';
let download_status = '';
function wait_request(){
    const server_download_Options = {
        uri: `http://${process.env.VUE_APP_flask_host}/getresult?mission-id=${mission_id}`,
        method: 'GET',
    };
    request(server_download_Options,function (error_wait,response_wait){
        if (error_wait){
            console.log(error_wait);
        }
        else{
            download_status = response_wait.body['mission-status'];
        }
    });
    return download_status;
}
//get mission id by sending the request to the flask backend server
app.get('/getmissionid',function (req, res){
    // send to flask server to get the mission id back
    var serverOptions = {
        uri: `http://flask:8000/getmissionid`,
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }

    request(serverOptions,function (error,response){
        console.log(response)
        res.json({missionID: JSON.parse(response.body)['mission-id']});
    });
});

//make directory when launch the server
app.post('/mkdir',(req,res)=>{
    mission_id = req.body.id;
    let file_loc = './upload';
    if (!fs.existsSync(file_loc)){
        fs.mkdirSync(file_loc);
    }
    file_loc += '/' + req.body.id;
    if (!fs.existsSync(file_loc)){
        fs.mkdirSync(file_loc);
    }
});

//Upload endpoint to process the uploaded files
app.post('/upload',function (req,res,next) {
    let file_loc = './upload/' + mission_id;
    //upload files into folder
    let fstream;
    req.pipe(req.busboy);
    req.busboy.on('file',function (fieldname,file,info){
        fstream = fs.createWriteStream(file_loc + '/' + info['filename']);
        file.pipe(fstream);
        fstream.on('close',function(){
            console.log('Upload Finished!');
        });
    });
    res.json({upload_status: 'Upload File!'});
});

// delete file
app.post('/delete',function (req,res){
    let file_loc = './upload/' + mission_id + '/' + req.body.deleteName;
    fs.unlink(file_loc,()=>{
        res.json({delete_status:'Delete!'});
    });
});

// save setting for merge
app.post('/merge_save',function (req, res){
    let task_Input = req.body.taskInput;
    let task_setting_from = [];
    let task_setting_to = [];
    for (let i = 0; i < task_Input.length; i++) {
        task_setting_from[i] = task_Input[i].from;
        task_setting_to[i] = task_Input[i].to;
      }
    res.json({save_status: 'Merge Saved!', save_data_from: [task_setting_from], save_data_to: [task_setting_to]});
});

// save setting for split
app.post('/split_save',function (req, res){
    let task_Input = req.body.taskInput;
    let task_setting_from = [];
    let task_setting_to = [];
    for (let i = 0; i < task_Input.length; i++) {
        task_setting_from[i] = task_Input[i].from;
        task_setting_to[i] = task_Input[i].to;
      }
    res.json({save_status: 'Split Saved!', save_data_from: [task_setting_from], save_data_to: [task_setting_to]});
});

//post request to flask backend server
app.post('/postrequest',function (req, res){

    const server_post_Options = {
        uri: `http://${process.env.VUE_APP_flask_host}/postrequest`,
        method: 'POST',
        json: req.body
    };
    request(server_post_Options,function (error,response){
        // determine whether to send request to obtain the downloaded link
        if(error){
            console.log(error);
        }
        else if(response.body['request-status'] === 'success') {
            // send another set of requests to keep asking whether the download is available
            // This will stop when the link is returned with status 'ready'
            this.interval = setInterval(() => wait_request(), 5000);
            if (download_status === 'finished') {
                window.clearInterval(this.interval);
                const download_Options = {
                    uri: `http://${process.env.VUE_APP_flask_host}/getdownloadlink`,
                    method: 'GET',
                };
                request(download_Options, function (error_download, response_download) {
                    // determine whether to send request to obtain the downloaded link
                    if (error_download) {
                        console.log(error_download);
                    }
                    else if(response_download.body['request-status'] === 'success'){
                        res.json({link:response_download.body['download-link'], download_status: 'Ready!'});
                    }
                    else{
                        console.log(response_download.body['Message']);
                    }
                });
            }
        }
        else{
            res.json({'internal error with request': 500});
        }
        res.json({status: response.body['request-status']});
    });
});
app.post('/debug',function (req,res){
   console.log(JSON.stringify(req.body.json_str));
   console.log(req.body.json_str);
});
app.listen(port, ()=>{console.log(`Server listening on port ${port}`)});