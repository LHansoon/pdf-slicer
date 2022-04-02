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
            console.log('done');
        });
    });
    res.json({upload_status: 'Upload File'});
});

app.listen(port, ()=>{console.log(`Server listening on port ${port}`)});