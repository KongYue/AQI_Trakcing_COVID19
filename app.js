const express = require('express');
const app = express();
const path = require('path');
const router = express.Router();
const fs = require('fs');
const util = require('util');

const dataprocess = require('./dataprocess');

router.get('/',function(req,res){
  res.sendFile(path.join(__dirname+'/public/index.html'));
});
router.get('/plot',async function(req,res){
  let data_result = await dataprocess.response_request(req.query);
  res.send(data_result);
});

router.get('/load',async function(req,res){
   //let data_result = await dataprocess.response_request(req.query,'python_init_load.py');
   const readFile = util.promisify(fs.readFile);
   readFile('./country_city.json').then(
     data=>{
      res.send(data);
     }
   )
 });
router.get('/about',function(req,res){
  res.sendFile(path.join(__dirname+'/about.html'));
});

router.get('/sitemap',function(req,res){
  res.sendFile(path.join(__dirname+'/sitemap.html'));
});

//add the router
app.use('/', router);

app.use(express.static("public"));
app.listen(process.env.port || 3000);

console.log('Running at Port 3000');