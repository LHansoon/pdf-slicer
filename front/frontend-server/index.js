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

//get mission id by sending the request to the flask backend server
app.get('/getmissionid',function (req, res){
    // send to flask server to get the mission id back
    request('http://localhost:8000/getmissionid',function (error,response){
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
    // send to flask server to get the mission id back
    request('http://localhost:8000/postrequest',function (error,response){
        res.json({status: JSON.parse(response.body)['request-status']});
    });
});
app.post('/debug',function (req,res){
   console.log(JSON.stringify(req.body.json_str));
   console.log(req.body.json_str);
});
app.listen(port, ()=>{console.log(`Server listening on port ${port}`)});