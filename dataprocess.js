const spawn = require("child_process").spawn;


async function response_request(req) {
  console.log(`This is response request function: ${JSON.stringify(req)}`);
  let d_s = await generate_user_requested_data(
    req.country,
    req.city,
    req.pollutant,
    'python_request_process.py'
  );
  return JSON.parse(d_s);
}

async function generate_user_requested_data(country, city, pollutant,script_name) {

  let options = {
    pythonPath: 'D:/home/python364x64/python',
    //********* * local use***********
    //pythonPath:'C:/Users/Nick Wang/AppData/Local/Programs/Python/Python38-32/python',
    scriptPath: 'D:/home/site/wwwroot',
    args:
    [
      country,
      city,
      pollutant
    ]
  };

  const child = spawn(options.pythonPath, [
    `./python/${script_name}`,
    country,
    city,
    pollutant,
  ]);


  let data = "";
    for await (const chunk of child.stdout) {
       // console.log('stdout chunk: '+chunk);
        data += chunk;
    }
    let error = "";
    for await (const chunk of child.stderr) {
       // console.error('stderr chunk: '+chunk);
        error += chunk;
    }
    const exitCode = await new Promise( (resolve, reject) => {
        child.on('close', resolve);
    });

    if( exitCode) {
        throw new Error( `subprocess error exit ${exitCode}, ${error}`);
    }
    return data;
}
module.exports.response_request = response_request;

