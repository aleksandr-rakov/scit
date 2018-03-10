var spawn = require('child_process').spawn;

var run_pserve=function() {
    var runserver = spawn(
        'pserve',
        ['development.ini', '--reload'], 
        { stdio: 'inherit' }
    );    
    runserver.on('close', function(code) {
        // if (code !== 0) {
        //     console.error('pserve exited with error code: ' + code);
        // } else {
        //     console.log('pserve exited normally.');
        // }
        setTimeout(run_pserve,1000);
        // run_pserve();
    });
};

module.exports = {
  devServer: {
    open: false,
    host: '0.0.0.0',
    port: 8080,
    https: false,
    hotOnly: false,
    proxy: {
        '/api/': {
            target: 'http://localhost:6543/'
        }
    },
    before: app => {
      // app is an express instance

      // when env is testing, don't need open it
      if (process.env.NODE_ENV !== 'testing') {
        // opn(uri)
        run_pserve();
      }
    }
  }
}