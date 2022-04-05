const express = require('express');
const cors = require('cors');
const fs = require('fs');
const fs_extra = require('fs-extra');
const bodyParser = require('body-parser')
const busboy = require('connect-busboy');

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
    let merge_task_setting = '';
    let task_no = '';
    let task_file = '';
    let task_Input = req.body.taskInput;
    let task_setting_from = [];
    let task_setting_to = [];
    task_no = req.body.taskNum.toString();
    task_file = req.body.taskFile;
    for (let i = 0; i < task_Input.length; i++) {
        task_setting_from[i] = task_Input[i].from;
        task_setting_to[i] = task_Input[i].to;
      }
    merge_task_setting = '"'+ task_no + '":{"file-name":' + '"' + task_file + '"'
    +',"inner-merge-order":{';
    for (let i = 0; i < task_Input.length; i++){
        let str_i = i.toString();
        merge_task_setting += '"' + str_i + '"' + ':{"from":' + task_setting_from[i] +
            ',"to":' + task_setting_to[i] + '},'
    }
    merge_task_setting = merge_task_setting.slice(0,-1);
    merge_task_setting += '}}';
    res.json({save_status: 'Merge Saved!', save_data: {merge_task_setting}});
});
app.listen(port, ()=>{console.log(`Server listening on port ${port}`)});